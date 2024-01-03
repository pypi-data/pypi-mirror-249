from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from typing import Any, Self, override
from uuid import uuid4

from dearpygui import dearpygui as dpg
from keyboard import add_hotkey
from pymem.exception import MemoryReadError, MemoryWriteError

from trainerbase.codeinjection import AbstractCodeInjection
from trainerbase.common import ShortLongPressSwitch, Switchable, Teleport
from trainerbase.gameobject import (
    GameBool,
    GameByte,
    GameDouble,
    GameFloat,
    GameInt,
    GameLongLong,
    GameObject,
    GameShort,
    GameUnsignedInt,
    GameUnsignedLongLong,
    GameUnsignedShort,
)
from trainerbase.scriptengine import Script
from trainerbase.speedhack import SpeedHack
from trainerbase.tts import say


class AbstractUIComponent(ABC):
    @abstractmethod
    def add_to_ui(self) -> None:
        pass


class SeparatorUI(AbstractUIComponent):
    @override
    def add_to_ui(self) -> None:
        dpg.add_separator()


class TextUI(AbstractUIComponent):
    def __init__(self, text: str):
        self.text = text

    @override
    def add_to_ui(self) -> None:
        dpg.add_text(self.text)


class ScriptUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "script__"

    def __init__(
        self,
        script: Script,
        label: str,
        hotkey: str | None = None,
        tts_on_hotkey: bool = True,
    ):
        self.script = script
        self.pure_label = label
        self.label_with_hotkey = label if hotkey is None else f"[{hotkey}] {label}"
        self.hotkey = hotkey
        self.tts_on_hotkey = tts_on_hotkey

        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @override
    def add_to_ui(self) -> None:
        if self.hotkey is not None:
            add_hotkey(self.hotkey, self.on_hotkey_press)

        dpg.add_checkbox(
            label=self.label_with_hotkey,
            tag=self.dpg_tag,
            callback=self.on_script_state_change,
            default_value=self.script.enabled,
        )

    def on_script_state_change(self):
        self.script.enabled = dpg.get_value(self.dpg_tag)

    def on_hotkey_press(self):
        dpg.set_value(self.dpg_tag, not dpg.get_value(self.dpg_tag))

        self.on_script_state_change()

        if self.tts_on_hotkey:
            status = "enabled" if self.script.enabled else "disabled"
            say(f"Script {self.pure_label} {status}")


class CodeInjectionUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "injection__"

    def __init__(
        self,
        injection: AbstractCodeInjection,
        label: str,
        hotkey: str | None = None,
        tts_on_hotkey: bool = True,
    ):
        self.injection = injection
        self.pure_label = label
        self.label_with_hotkey = label if hotkey is None else f"[{hotkey}] {label}"
        self.hotkey = hotkey
        self.tts_on_hotkey = tts_on_hotkey

        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @override
    def add_to_ui(self) -> None:
        if self.hotkey is not None:
            add_hotkey(self.hotkey, self.on_hotkey_press)

        dpg.add_checkbox(label=self.label_with_hotkey, tag=self.dpg_tag, callback=self.on_codeinjection_state_change)

    def on_codeinjection_state_change(self):
        if dpg.get_value(self.dpg_tag):
            change_codeinjection_state = self.injection.inject
        else:
            change_codeinjection_state = self.injection.eject

        try:
            change_codeinjection_state()
        except (MemoryReadError, MemoryWriteError):
            dpg.set_value(self.dpg_tag, not dpg.get_value(self.dpg_tag))

    def on_hotkey_press(self):
        dpg.set_value(self.dpg_tag, not dpg.get_value(self.dpg_tag))
        self.on_codeinjection_state_change()

        if self.tts_on_hotkey:
            status = "applied" if dpg.get_value(self.dpg_tag) else "removed"
            say(f"CodeInjection {self.pure_label} {status}")


class GameObjectUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "object__"
    DPG_TAG_POSTFIX_IS_FROZEN = "__frozen"
    DPG_TAG_POSTFIX_GETTER = "__getter"
    DPG_TAG_POSTFIX_SETTER = "__setter"

    displayed_objects: list[Self] = []

    def __init__(
        self,
        gameobject: GameObject,
        label: str,
        hotkey: str | None = None,
        default_setter_input_value: Any = 0,
        before_set: Callable | None = None,
        tts_on_hotkey: bool = True,
        setter_input_width: int = 220,
    ):
        if not gameobject.is_tracked:
            hotkey = None

        self.gameobject = gameobject
        self.pure_label = label
        self.label_with_hotkey = label if hotkey is None else f"[{hotkey}] {label}"
        self.hotkey = hotkey
        self.default_setter_input_value = default_setter_input_value
        self.before_set = before_set
        self.tts_on_hotkey = tts_on_hotkey
        self.setter_input_width = setter_input_width

        dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"
        self.dpg_tag_frozen = f"{dpg_tag}{self.DPG_TAG_POSTFIX_IS_FROZEN}"
        self.dpg_tag_getter = f"{dpg_tag}{self.DPG_TAG_POSTFIX_GETTER}"
        self.dpg_tag_setter = f"{dpg_tag}{self.DPG_TAG_POSTFIX_SETTER}"

    @override
    def add_to_ui(self) -> None:
        if self.hotkey is not None:
            add_hotkey(self.hotkey, self.on_hotkey_press)

        with dpg.group(horizontal=True):
            if self.gameobject.is_tracked:
                dpg.add_checkbox(tag=self.dpg_tag_frozen, callback=self.on_frozen_state_change)

            dpg.add_text(self.label_with_hotkey)
            dpg.add_input_text(width=220, tag=self.dpg_tag_getter, readonly=True)

            self.add_setter_input()

            dpg.add_button(label="Set", callback=self.on_value_set)

        GameObjectUI.displayed_objects.append(self)

    def add_setter_input(self):
        default_kwargs = {
            "tag": self.dpg_tag_setter,
            "width": self.setter_input_width,
            "default_value": self.default_setter_input_value,
        }

        if self.gameobject.value_range is not None:
            min_value, max_value = self.gameobject.value_range
            default_kwargs["min_clamped"] = True
            default_kwargs["max_clamped"] = True
            default_kwargs["min_value"] = min_value
            default_kwargs["max_value"] = max_value

        match self.gameobject:
            case GameFloat():
                dpg.add_input_float(**default_kwargs)
            case GameDouble():
                dpg.add_input_double(**default_kwargs)
            case (
                GameByte()
                | GameShort()
                | GameInt()
                | GameLongLong()
                | GameUnsignedShort()
                | GameUnsignedInt()
                | GameUnsignedLongLong()
            ):
                # There is no input for integers that are not simple `signed long int`.
                # TODO: Use better input component if it's already added to dpg. Remove this crutch.

                min_value = default_kwargs.pop("min_value", GameInt.value_range[0])
                max_value = default_kwargs.pop("max_value", GameInt.value_range[1])

                if self.gameobject.value_range is not None:
                    min_value = max(min_value, GameInt.value_range[0])
                    max_value = min(max_value, GameInt.value_range[1])

                dpg.add_input_int(min_value=min_value, max_value=max_value, **default_kwargs)
            case GameBool():
                dpg.add_checkbox(
                    tag=self.dpg_tag_setter,
                    default_value=bool(self.default_setter_input_value),
                )
            case _:
                dpg.add_input_text(**default_kwargs)

    def on_frozen_state_change(self):
        try:
            self.gameobject.frozen = self.gameobject.value if dpg.get_value(self.dpg_tag_frozen) else None
        except MemoryReadError:
            dpg.set_value(self.dpg_tag_frozen, False)

    def on_value_set(self):
        raw_new_value = dpg.get_value(self.dpg_tag_setter)
        new_value = raw_new_value if self.before_set is None else self.before_set(raw_new_value)

        if self.gameobject.frozen is None:
            try:
                self.gameobject.value = new_value
            except (MemoryWriteError, ValueError):
                pass
        else:
            self.gameobject.frozen = new_value

    def on_hotkey_press(self):
        dpg.set_value(self.dpg_tag_frozen, not dpg.get_value(self.dpg_tag_frozen))

        self.on_frozen_state_change()

        if self.tts_on_hotkey:
            status = "released" if self.gameobject.frozen is None else "frozen"
            say(f"GameObject {self.pure_label} {status}")


class TeleportUI(AbstractUIComponent):
    DPG_TAG_TELEPORT_LABELS = "__teleport_labels"

    def __init__(
        self,
        tp: Teleport,
        hotkey_save_position: str | None = "Insert",
        hotkey_set_saved_position: str | None = "Home",
        hotkey_dash: str | None = "End",
        tts_on_hotkey: bool = True,
    ):
        self.tp = tp
        self.hotkey_save_position = hotkey_save_position
        self.hotkey_set_saved_position = hotkey_set_saved_position
        self.hotkey_dash = hotkey_dash
        self.tts_on_hotkey = tts_on_hotkey

    @override
    def add_to_ui(self) -> None:
        self._tp_add_save_set_position_hotkeys_if_needed()
        self._tp_add_dash_hotkeys_if_needed()

        add_components(
            GameObjectUI(self.tp.player_x, "X"),
            GameObjectUI(self.tp.player_y, "Y"),
            GameObjectUI(self.tp.player_z, "Z"),
        )

        self._tp_add_labels_if_needed()

        dpg.add_button(label="Clip Coords", callback=self.on_clip_coords)

    def on_clip_coords(self):
        dpg.set_clipboard_text(repr(self.tp.get_coords()))

    def on_hotkey_save_position_press(self):
        self.tp.save_position()

        if self.tts_on_hotkey:
            say("Position saved")

    def on_hotkey_set_saved_position_press(self):
        is_position_restored = self.tp.restore_saved_position()

        if self.tts_on_hotkey:
            say("Position restored" if is_position_restored else "Save position at first")

    def on_hotkey_dash_press(self):
        self.tp.dash()
        if self.tts_on_hotkey:
            say("Dash!")

    def on_goto_label(self):
        self.tp.goto(dpg.get_value(self.DPG_TAG_TELEPORT_LABELS))

    def _tp_add_save_set_position_hotkeys_if_needed(self):
        if self.hotkey_save_position is None or self.hotkey_set_saved_position is None:
            return

        add_hotkey(self.hotkey_save_position, self.on_hotkey_save_position_press)
        add_hotkey(self.hotkey_set_saved_position, self.on_hotkey_set_saved_position_press)

        dpg.add_text(f"[{self.hotkey_save_position}] Save Position")
        dpg.add_text(f"[{self.hotkey_set_saved_position}] Restore Position")

    def _tp_add_dash_hotkeys_if_needed(self):
        if self.hotkey_dash is None:
            return

        add_hotkey(self.hotkey_dash, self.on_hotkey_dash_press)

        dpg.add_text(f"[{self.hotkey_dash}] Dash")

    def _tp_add_labels_if_needed(self):
        if not self.tp.labels:
            return

        labels = sorted(self.tp.labels.keys())

        with dpg.group(horizontal=True):
            dpg.add_button(label="Go To", callback=self.on_goto_label)
            dpg.add_combo(label="Labels", tag=self.DPG_TAG_TELEPORT_LABELS, items=labels, default_value=labels[0])


class SpeedHackUI(AbstractUIComponent):
    DPG_TAG_SPEEDHACK_FACTOR_INPUT = "tag_speedhack_factor_input"
    DPG_TAG_SPEEDHACK_PRESET_INPUT = "tag_speedhack_preset_input"

    PRESETS: tuple[float, ...] = (0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 50.0)

    def __init__(
        self, speedhack: SpeedHack | None = None, key: str = "Delete", default_factor_input_value: float = 3.0
    ):
        self.speedhack = SpeedHack() if speedhack is None else speedhack
        self.key = key
        self.default_factor_input_value = default_factor_input_value
        self.switch = ShortLongPressSwitch(SpeedHackUISwitch(self.speedhack, self.DPG_TAG_SPEEDHACK_FACTOR_INPUT), key)

    @override
    def add_to_ui(self) -> None:
        dpg.add_text(f"Hold [{self.key}] Enable SpeedHack")
        dpg.add_text(f"Press [{self.key}] Toggle SpeedHack")

        dpg.add_input_double(
            tag=self.DPG_TAG_SPEEDHACK_FACTOR_INPUT,
            label="SpeedHack Factor",
            min_value=0.0,
            max_value=100.0,
            default_value=self.default_factor_input_value,
            min_clamped=True,
            max_clamped=True,
            callback=self.on_factor_change,
        )

        dpg.add_slider_int(
            tag=self.DPG_TAG_SPEEDHACK_PRESET_INPUT,
            label="Preset",
            min_value=0,
            max_value=len(self.PRESETS) - 1,
            clamped=True,
            default_value=self.get_closest_preset_index(self.default_factor_input_value),
            callback=self.on_preset_change,
        )

        self.switch.handle()

    def on_preset_change(self):
        new_factor = self.PRESETS[dpg.get_value(self.DPG_TAG_SPEEDHACK_PRESET_INPUT)]
        dpg.set_value(self.DPG_TAG_SPEEDHACK_FACTOR_INPUT, new_factor)

    def on_factor_change(self):
        new_factor = dpg.get_value(self.DPG_TAG_SPEEDHACK_FACTOR_INPUT)
        closest_preset_index = self.get_closest_preset_index(new_factor)
        dpg.set_value(self.DPG_TAG_SPEEDHACK_PRESET_INPUT, closest_preset_index)

    def get_closest_preset_index(self, factor: float) -> int:
        closest_preset = min(self.PRESETS, key=lambda preset: abs(preset - factor))
        return self.PRESETS.index(closest_preset)


class SpeedHackUISwitch(Switchable):
    def __init__(self, speedhack: SpeedHack, dpg_tag: str):
        self.speedhack = speedhack
        self.dpg_tag = dpg_tag

    @override
    def enable(self):
        self.speedhack.factor = dpg.get_value(self.dpg_tag)

    @override
    def disable(self):
        self.speedhack.factor = 1.0


def add_components(*components: AbstractUIComponent):
    for component in components:
        component.add_to_ui()


def simple_trainerbase_menu(window_title: str, width: int, height: int):
    def menu_decorator(initializer: Callable):
        @wraps(initializer)
        def run_menu_wrapper(on_initialized: Callable):
            dpg.create_context()
            dpg.create_viewport(
                title=window_title,
                min_width=width,
                min_height=height,
                width=width,
                height=height,
            )
            dpg.setup_dearpygui()

            with dpg.window(
                label=window_title,
                tag="menu",
                min_size=[width, height],
                no_close=True,
                no_move=True,
                no_title_bar=True,
                horizontal_scrollbar=True,
            ):
                initializer()

            dpg.show_viewport()

            on_initialized()

            dpg.start_dearpygui()
            dpg.destroy_context()

        return run_menu_wrapper

    return menu_decorator


def update_displayed_objects():
    for game_object_ui in GameObjectUI.displayed_objects:
        try:
            new_value = game_object_ui.gameobject.value
        except MemoryReadError:
            new_value = "<Unresolved>"

        dpg.set_value(game_object_ui.dpg_tag_getter, new_value)
