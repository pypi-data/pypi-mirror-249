import argparse
import logging
import re
import select
import sys
import time
from threading import Event as TEvent
from typing import Sequence, Literal

from hhd.controller import Button, Consumer, Event, Producer
from hhd.controller.base import Multiplexer, TouchpadAction
from hhd.controller.lib.hid import enumerate_unique
from hhd.controller.physical.evdev import B as EC
from hhd.controller.physical.evdev import GenericGamepadEvdev, unhide_all
from hhd.controller.physical.hidraw import GenericGamepadHidraw
from hhd.controller.physical.imu import AccelImu, GyroImu
from hhd.controller.virtual.ds5 import DualSense5Edge, TouchpadCorrectionType
from hhd.controller.virtual.uinput import (
    UInputDevice,
    HHD_PID_VENDOR,
    HHD_PID_GAMEPAD,
    MOTION_AXIS_MAP,
    MOTION_CAPABILITIES,
    HHD_PID_MOTION,
    HHD_PID_TOUCHPAD,
    TOUCHPAD_CAPABILITIES,
    TOUCHPAD_AXIS_MAP,
    TOUCHPAD_BUTTON_MAP,
)
from hhd.plugins import Config, Context, Emitter

from .const import (
    LGO_RAW_INTERFACE_AXIS_MAP,
    LGO_RAW_INTERFACE_BTN_ESSENTIALS,
    LGO_RAW_INTERFACE_BTN_MAP,
    LGO_RAW_INTERFACE_CONFIG_MAP,
    LGO_TOUCHPAD_AXIS_MAP,
    LGO_TOUCHPAD_BUTTON_MAP,
)
from .gyro_fix import GyroFixer
from .hid import rgb_callback

ERROR_DELAY = 1
SELECT_TIMEOUT = 1

logger = logging.getLogger(__name__)

LEN_VID = 0x17EF
LEN_PIDS = {
    0x6182: "xinput",
    0x6183: "dinput",
    0x6184: "dual_dinput",
    0x6185: "fps",
}


def plugin_run(conf: Config, emit: Emitter, context: Context, should_exit: TEvent):
    # Remove leftover udev rules
    # unhide_all()
    if (gyro_fix := conf.get("gyro_fix", False)) and conf["gyro"].to(bool):
        gyro_fixer = GyroFixer(int(gyro_fix) if int(gyro_fix) > 10 else 100)
    else:
        gyro_fixer = None

    while not should_exit.is_set():
        try:
            controller_mode = None
            pid = None
            while not controller_mode:
                devs = enumerate_unique(LEN_VID)
                if not devs:
                    logger.error(
                        f"Legion go controllers not found, waiting {ERROR_DELAY}s."
                    )
                    time.sleep(ERROR_DELAY)
                    continue

                for d in devs:
                    if d["product_id"] in LEN_PIDS:
                        pid = d["product_id"]
                        controller_mode = LEN_PIDS[pid]
                        break
                else:
                    logger.error(
                        f"Legion go controllers not found, waiting {ERROR_DELAY}s."
                    )
                    time.sleep(ERROR_DELAY)
                    continue

            if (
                controller_mode == "xinput"
                and conf["xinput.mode"].to(str) != "disabled"
            ):
                logger.info("Launching emulated controller.")
                if gyro_fixer:
                    gyro_fixer.open()
                controller_loop_xinput(conf, should_exit)
            else:
                if controller_mode != "xinput":
                    logger.info(
                        f"Controllers in non-supported (yet) mode: {controller_mode}."
                    )
                else:
                    logger.info(
                        f"Controllers in xinput mode but emulation is disabled."
                    )
                controller_loop_rest(
                    controller_mode, pid if pid else 2, conf, should_exit
                )
        except Exception as e:
            logger.error(f"Received the following error:\n{e}")
            logger.error(
                f"Assuming controllers disconnected, restarting after {ERROR_DELAY}s."
            )
            # Raise exception
            if conf.get("debug", False):
                raise e
            time.sleep(ERROR_DELAY)
        finally:
            if gyro_fixer:
                gyro_fixer.close()
            # Remove leftover udev rules
            # unhide_all()


def controller_loop_rest(mode: str, pid: int, conf: Config, should_exit: TEvent):
    debug = conf.get("debug", False)
    shortcuts_enabled = conf["shortcuts"].to(bool)
    # FIXME: Sleep when shortcuts are disabled instead of polling raw interface
    if shortcuts_enabled:
        logger.info(f"Launching a shortcuts device.")
    else:
        logger.info(f"Shortcuts disabled. Waiting for controllers to change modes.")

    d_raw = SelectivePassthrough(
        GenericGamepadHidraw(
            vid=[LEN_VID],
            pid=list(LEN_PIDS),
            usage_page=[0xFFA0],
            usage=[0x0001],
            report_size=64,
            axis_map=LGO_RAW_INTERFACE_AXIS_MAP,
            btn_map=LGO_RAW_INTERFACE_BTN_MAP,
            required=True,
        )
    )

    multiplexer = Multiplexer(
        dpad="analog_to_discrete",
        trigger="analog_to_discrete",
        share_to_qam=conf["share_to_qam"].to(bool),
    )
    d_uinput = UInputDevice(
        name=f"HHD Shortcuts (Legion Mode: {mode})",
        pid=HHD_PID_VENDOR | 0x0200 | (pid & 0xF),
        phys=f"phys-hhd-shortcuts-legion-{mode}",
    )

    d_shortcuts = GenericGamepadEvdev(
        vid=[LEN_VID],
        pid=list(LEN_PIDS),
        name=[re.compile(r"Legion-Controller \d-.. Keyboard")],
        capabilities={EC("EV_KEY"): [EC("KEY_1")]},
        required=True,
    )

    try:
        fds = []
        fds.extend(d_raw.open())
        if shortcuts_enabled:
            fds.extend(d_shortcuts.open())
            fds.extend(d_uinput.open())

        while not should_exit.is_set():
            select.select(fds, [], [], SELECT_TIMEOUT)
            evs = multiplexer.process(d_raw.produce(fds))

            if shortcuts_enabled:
                d_shortcuts.produce(fds)
                d_uinput.produce(fds)
                if debug and evs:
                    logger.info(evs)
                d_uinput.consume(evs)
    finally:
        d_uinput.close(True)
        d_shortcuts.close(True)
        d_raw.close(True)


def controller_loop_xinput(conf: Config, should_exit: TEvent):
    debug = conf.get("debug", False)

    # Output
    ds5_touch = conf["xinput.ds5e.touchpad"].to(bool)
    xmode = conf["xinput.mode"].to(str)
    match xmode:
        case "ds5e":
            d_out = DualSense5Edge(
                touchpad_method=conf["touchpad.emulation.correction"].to(
                    TouchpadCorrectionType
                ),
                enable_touchpad=ds5_touch,
            )
            d_out2 = None
        case _:
            d_out = UInputDevice(phys="phys-hhd-legion")
            if conf["accel"].to(bool) | conf["gyro"].to(bool):
                d_out2 = UInputDevice(
                    name="Handheld Daemon Controller Motion Sensors",
                    phys="phys-hhd-legion",
                    capabilities=MOTION_CAPABILITIES,
                    pid=HHD_PID_MOTION,
                    btn_map={},
                    axis_map=MOTION_AXIS_MAP,
                    output_imu_timestamps=True,
                )
            else:
                d_out2 = None

    if conf["touchpad.mode"].to(str) == "emulation" and (
        xmode != "ds5e" or not ds5_touch
    ):
        d_out_touch = UInputDevice(
            name="Handheld Daemon Touchpad",
            phys="phys-hhd-legion",
            capabilities=TOUCHPAD_CAPABILITIES,
            pid=HHD_PID_TOUCHPAD,
            btn_map=TOUCHPAD_BUTTON_MAP,
            axis_map=TOUCHPAD_AXIS_MAP,
            output_timestamps=True,
        )
    else:
        d_out_touch = None

    # Imu
    d_accel = AccelImu()
    d_gyro = GyroImu()

    # Inputs
    d_xinput = GenericGamepadEvdev(
        vid=[0x17EF],
        pid=[0x6182],
        # name=["Generic X-Box pad"],
        capabilities={EC("EV_KEY"): [EC("BTN_A")]},
        required=True,
        hide=True,
    )
    d_touch = GenericGamepadEvdev(
        vid=[0x17EF],
        pid=[0x6182],
        # name=["  Legion Controller for Windows  Touchpad"],
        capabilities={EC("EV_KEY"): [EC("BTN_MOUSE")]},
        btn_map=LGO_TOUCHPAD_BUTTON_MAP,
        axis_map=LGO_TOUCHPAD_AXIS_MAP,
        aspect_ratio=1,
        required=True,
    )
    d_raw = SelectivePassthrough(
        GenericGamepadHidraw(
            vid=[LEN_VID],
            pid=list(LEN_PIDS),
            usage_page=[0xFFA0],
            usage=[0x0001],
            report_size=64,
            axis_map=LGO_RAW_INTERFACE_AXIS_MAP,
            btn_map=LGO_RAW_INTERFACE_BTN_MAP,
            config_map=LGO_RAW_INTERFACE_CONFIG_MAP,
            callback=rgb_callback if conf["xinput.ds5e.led_support"].to(bool) else None,
            required=True,
        )
    )
    # Mute keyboard shortcuts, mute
    d_shortcuts = GenericGamepadEvdev(
        vid=[LEN_VID],
        pid=list(LEN_PIDS),
        # name=["  Legion Controller for Windows  Keyboard"],
        capabilities={EC("EV_KEY"): [EC("KEY_1")]},
        # report_size=64,
        required=True,
    )

    match conf["swap_legion"].to(str):
        case "disabled":
            swap_guide = None
        case "l_is_start":
            swap_guide = "guide_is_start"
        case "l_is_select":
            swap_guide = "guide_is_select"
        case val:
            assert False, f"Invalid value for `swap_legion`: {val}"

    multiplexer = Multiplexer(
        swap_guide=swap_guide,
        trigger="analog_to_discrete",
        dpad="analog_to_discrete",
        led="main_to_sides",
        status="both_to_main",
        share_to_qam=conf["share_to_qam"].to(bool),
        touchpad_short=conf["touchpad.emulation.short"].to(TouchpadAction),
        touchpad_right=conf["touchpad.emulation.hold"].to(TouchpadAction),
    )

    REPORT_FREQ_MIN = 25
    REPORT_FREQ_MAX = 400

    REPORT_DELAY_MAX = 1 / REPORT_FREQ_MIN
    REPORT_DELAY_MIN = 1 / REPORT_FREQ_MAX

    fds = []
    devs = []
    fd_to_dev = {}

    def prepare(m):
        devs.append(m)
        fs = m.open()
        fds.extend(fs)
        for f in fs:
            fd_to_dev[f] = m

    try:
        prepare(d_xinput)
        if conf.get("accel", False):
            prepare(d_accel)
        if conf.get("gyro", False):
            prepare(d_gyro)
        prepare(d_shortcuts)
        if conf["touchpad.mode"].to(str) == "emulation":
            prepare(d_touch)
        prepare(d_raw)
        if d_out_touch:
            prepare(d_out_touch)
        prepare(d_out)
        if d_out2:
            prepare(d_out2)

        logger.info("Emulated controller launched, have fun!")
        while not should_exit.is_set():
            start = time.perf_counter()
            # Add timeout to call consumers a minimum amount of times per second
            r, _, _ = select.select(fds, [], [], REPORT_DELAY_MAX)
            evs = []
            to_run = set()
            for f in r:
                to_run.add(id(fd_to_dev[f]))

            for d in devs:
                if id(d) in to_run:
                    evs.extend(d.produce(r))

            evs = multiplexer.process(evs)
            if evs:
                if debug:
                    logger.info(evs)

                d_xinput.consume(evs)
                d_raw.consume(evs)
                d_out.consume(evs)
                if d_out2:
                    d_out2.consume(evs)
                if d_out_touch:
                    d_out_touch.consume(evs)

            # If unbounded, the total number of events per second is the sum of all
            # events generated by the producers.
            # For Legion go, that would be 100 + 100 + 500 + 30 = 730
            # Since the controllers of the legion go only update at 500hz, this is
            # wasteful.
            # By setting a target refresh rate for the report and sleeping at the
            # end, we ensure that even if multiple fds become ready close to each other
            # they are combined to the same report, limiting resource use.
            # Ideally, this rate is smaller than the report rate of the hardware controller
            # to ensure there is always a report from that ready during refresh
            t = time.perf_counter()
            elapsed = t - start
            if elapsed < REPORT_DELAY_MIN:
                time.sleep(REPORT_DELAY_MIN - elapsed)

    except KeyboardInterrupt:
        raise
    finally:
        for d in reversed(devs):
            d.close(True)


class SelectivePassthrough(Producer, Consumer):
    def __init__(
        self,
        parent,
        forward_buttons: Sequence[Button] = ("share", "mode"),
        passthrough: Sequence[Button] = list(
            next(iter(LGO_RAW_INTERFACE_BTN_ESSENTIALS.values()))
        ),
    ):
        self.parent = parent
        self.state = False

        self.forward_buttons = forward_buttons
        self.passthrough = passthrough

        self.to_disable_btn = set()
        self.to_disable_axis = set()

    def open(self) -> Sequence[int]:
        return self.parent.open()

    def close(self, exit: bool) -> bool:
        return super().close(exit)

    def produce(self, fds: Sequence[int]) -> Sequence[Event]:
        evs: Sequence[Event] = self.parent.produce(fds)

        out = []
        prev_state = self.state
        for ev in evs:
            if ev["type"] == "button" and ev["code"] in self.forward_buttons:
                self.state = ev.get("value", False)

            if ev["type"] == "configuration":
                out.append(ev)
            elif ev["type"] == "button" and ev["code"] in self.passthrough:
                out.append(ev)
            elif ev["type"] == "button":
                self.to_disable_btn.add(ev["code"])
            elif ev["type"] == "axis":
                self.to_disable_axis.add(ev["code"])

        if self.state:
            # If mode is pressed, forward all events
            return evs
        elif prev_state:
            # If prev_state, meaning the user released the mode or share button
            # turn off all buttons that were pressed during it
            for btn in self.to_disable_btn:
                out.append({"type": "button", "code": btn, "value": False})
            self.to_disable_btn = set()
            for axis in self.to_disable_axis:
                out.append({"type": "axis", "code": axis, "value": 0})
            self.to_disable_axis = set()
            return out
        else:
            # Otherwise, just return the standard buttons
            return out

    def consume(self, events: Sequence[Event]):
        return self.parent.consume(events)
