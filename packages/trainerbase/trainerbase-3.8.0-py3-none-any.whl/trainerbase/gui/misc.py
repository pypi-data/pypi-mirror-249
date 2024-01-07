from typing import override
from uuid import uuid4

from dearpygui import dearpygui as dpg

from trainerbase.common.keyboard import AbstractKeyboardSwitch
from trainerbase.gui.types import AbstractUIComponent


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


class HotkeySwitchUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "switch__"

    def __init__(
        self,
        switch: AbstractKeyboardSwitch,
        label: str,
    ):
        self.switch = switch
        self.label_with_hotkey = f"[{switch.hotkey}] {label}"
        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @override
    def add_to_ui(self) -> None:
        dpg.add_text(self.label_with_hotkey, tag=self.dpg_tag)
        self.switch.handle()
