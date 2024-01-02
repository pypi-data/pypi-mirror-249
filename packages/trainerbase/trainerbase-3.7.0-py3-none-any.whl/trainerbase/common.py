from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence
from itertools import repeat, starmap
from math import sqrt
from operator import add, mul
from time import time
from typing import Self
from uuid import uuid4

from keyboard import on_press_key, on_release_key
from pymem.exception import MemoryReadError

from trainerbase.gameobject import AbstractReadableObject, GameObject
from trainerbase.memory import POINTER_SIZE, Address, allocate_pointer, pm
from trainerbase.scriptengine import Script, system_script_engine


type Coords[T: (int, float)] = tuple[T, T, T]
type Number = int | float


class Vector3:
    def __init__(self, x: Number, y: Number, z: Number):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __abs__(self) -> Number:
        return sqrt(sum(d * d for d in self))

    def __mul__(self, other) -> Self:
        return self.__apply_binary_function(other, mul)

    def __add__(self, other) -> Self:
        return self.__apply_binary_function(other, add)

    def __apply_binary_function(self, other, function) -> Self:
        if isinstance(other, (float, int)):
            other = repeat(other, 3)
        elif not isinstance(other, self.__class__):
            raise TypeError(f"Can't apply function {function}. Wrong type: {type(other)}")

        return self.__class__(*starmap(function, zip(self, other)))

    @classmethod
    def from_coords(cls, x1, y1, z1, x2, y2, z2) -> Self:
        return cls(x2 - x1, y2 - y1, z2 - z1)

    def get_normalized(self) -> Self:
        length = abs(self)
        return self.__class__(*(d / length for d in self))


class Teleport:
    def __init__(
        self,
        player_x: GameObject,
        player_y: GameObject,
        player_z: GameObject,
        labels: dict[str, Coords] | None = None,
        dash_coefficients: Vector3 | None = None,
        minimal_movement_vector_length: float = 0.1,
    ):
        self.player_x = player_x
        self.player_y = player_y
        self.player_z = player_z
        self.labels = {} if labels is None else labels

        self.saved_position: Coords | None = None

        self.dash_coefficients = Vector3(5, 5, 5) if dash_coefficients is None else dash_coefficients
        self.previous_position: Coords | None = None
        self.current_position: Coords | None = None
        self.movement_vector = Vector3(0, 0, 0)
        self.minimal_movement_vector_length = minimal_movement_vector_length

        system_script_engine.register_script(Script(self.update_movement_vector, enabled=True))

    def set_coords(self, x: Number, y: Number, z: Number = 100) -> None:
        self.player_x.value = x
        self.player_y.value = y
        self.player_z.value = z

    def get_coords(self) -> Coords:
        return self.player_x.value, self.player_y.value, self.player_z.value

    def goto(self, label: str) -> None:
        self.set_coords(*self.labels[label])

    def save_position(self) -> None:
        self.saved_position = self.get_coords()

    def restore_saved_position(self) -> bool:
        """
        Returns False if position is not saved else True
        """

        if self.saved_position is None:
            return False

        self.set_coords(*self.saved_position)

        return True

    def update_movement_vector(self) -> None:
        try:
            self.current_position = self.get_coords()
        except MemoryReadError:
            return

        if self.previous_position is None:
            self.previous_position = self.current_position
            return

        movement_vector = Vector3.from_coords(*self.previous_position, *self.current_position)

        if abs(movement_vector) < self.minimal_movement_vector_length:
            return

        self.movement_vector = movement_vector.get_normalized()
        self.previous_position = self.current_position

    def dash(self) -> None:
        dash_movement_vector = self.movement_vector * self.dash_coefficients
        new_coords = Vector3(*self.get_coords()) + dash_movement_vector
        self.set_coords(*new_coords)


class Switchable(ABC):
    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass


class ShortLongPressSwitch:
    def __init__(self, switchable: Switchable, key: str, short_press_max_delta: float = 0.3):
        self._key = key
        self._press_timestamp = None
        self._short_press_max_delta = short_press_max_delta
        self._switchable = switchable
        self._enabled = False

    def _on_press(self, _):
        if self._press_timestamp is None:
            self._press_timestamp = time()
        self.on_press()

    def _on_release(self, _):
        if self._is_short_delta():
            self.on_short_press()
        else:
            self.on_long_press()

        self._press_timestamp = None

    def _get_press_delta(self):
        if self._press_timestamp is None:
            return 0

        return time() - self._press_timestamp

    def _is_short_delta(self):
        return self._get_press_delta() <= self._short_press_max_delta

    def handle(self):
        on_release_key(self._key, self._on_release)
        on_press_key(self._key, self._on_press)

    def on_press(self):
        self._switchable.enable()

    def on_short_press(self):
        if self._enabled:
            self._enabled = False
            self._switchable.disable()
        else:
            self._enabled = True
            self._switchable.enable()

    def on_long_press(self):
        self._enabled = False
        self._switchable.disable()


class ASMArrayManager(Sequence):
    def __init__(
        self,
        array_length: int,
        element_size: int,
        offsets: None | list[int] = None,
        add: int = 0,
    ) -> None:
        if offsets:
            assert element_size == POINTER_SIZE, "If `offsets` is not None, `element_size` must be `POINTER_SIZE`"

        self.array_length = array_length
        self.element_size = element_size
        self.offsets = [] if offsets is None else offsets
        self.add = add

        self.array_address = pm.allocate(array_length * element_size)
        self.array_index_pointer = allocate_pointer()

    def __len__(self) -> int:
        return self.array_length

    def __getitem__(self, index: int) -> Address:
        element_address = self.get_pointer_to_element(index)
        target_address = Address(element_address, self.offsets, self.add)

        return Address(target_address.resolve())

    def __iter__(self) -> Iterator[Address]:
        for index in range(len(self)):
            yield self[index]

    def get_pointer_to_element(self, index: int) -> int:
        return self.array_address + self.element_size * index

    def generate_asm_append_code(self, from_register: str) -> str:
        array_address_register = "rbx" if pm.is_64_bit else "ebx"
        array_index_register = "rcx" if pm.is_64_bit else "ecx"
        reserve_register = "rax" if pm.is_64_bit else "eax"

        if from_register == array_address_register:
            array_address_register = reserve_register

        if from_register == array_index_register:
            array_index_register = reserve_register

        assert len({from_register, array_address_register, array_index_register}) == 3, "Registers must be unique"

        label_continue = f"__label_continue_{uuid4().hex}"

        asm = f"""
            push {array_address_register}
            push {array_index_register}

            mov {array_address_register}, {self.array_address}
            mov {array_index_register}, [{self.array_index_pointer}]

            mov [{array_address_register} + {array_index_register} * {self.element_size}], {from_register}

            inc {array_index_register}

            cmp {array_index_register}, {self.array_length}
            jl {label_continue}

            mov {array_index_register}, 0

            {label_continue}:

            mov [{self.array_index_pointer}], {array_index_register}

            pop {array_index_register}
            pop {array_address_register}
        """

        return asm


def regenerate(
    current_value: GameObject,
    max_value: AbstractReadableObject,
    percent: Number,
    min_value: Number = 1,
):
    if current_value.value < max_value.value:
        current_value.value += max(round(max_value.value * percent / 100), min_value)
