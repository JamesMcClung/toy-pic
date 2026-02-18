from typing import Self


class Vec3[T]:
    _vals: tuple[T, T, T]

    def __init__(self, x: T, y: T, z: T, *, dtype: type[T] | None = None):
        self._vals = (x, y, z)

        if dtype is None:
            if x.__class__ is y.__class__ is z.__class__:
                dtype = x.__class__
            else:
                raise Exception("unspecified and inconsistent dtype")

        self._dtype = dtype

    def __iter__(self):
        yield from self._vals

    def __getitem__(self, d: int) -> T:
        return self._vals[d]

    def __setitem__(self, d: int, val: T):
        self._vals[d] = val

    def copy(self) -> Self:
        return Self(self.x, self.y, self.z)

    @property
    def x(self) -> T:
        return self[0]

    @property
    def y(self) -> T:
        return self[1]

    @property
    def z(self) -> T:
        return self[2]

    @x.setter
    def x(self, val: T):
        self[0] = val

    @y.setter
    def y(self, val: T):
        self[1] = val

    @z.setter
    def z(self, val: T):
        self[2] = val

    def __add__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, self._dtype):
            return Self(self.x + other, self.y + other, self.z + other)
        else:
            return NotImplemented

    def __sub__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, self._dtype):
            return Self(self.x - other, self.y - other, self.z - other)
        else:
            return NotImplemented

    def __mul__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, self._dtype):
            return Self(self.x * other, self.y * other, self.z * other)
        else:
            return NotImplemented

    def __truediv__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, self._dtype):
            return Self(self.x / other, self.y / other, self.z / other)
        else:
            return NotImplemented

    def __div__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(self.x // other.x, self.y // other.y, self.z // other.z)
        elif isinstance(other, self._dtype):
            return Self(self.x // other, self.y // other, self.z // other)
        else:
            return NotImplemented

    def __rtruediv__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(other.x / self.x, other.y / self.y, other.z / self.z)
        elif isinstance(other, self._dtype):
            return Self(other / self.x, other / self.y, other / self.z)
        else:
            return NotImplemented

    def __rdiv__(self, other: Self | T) -> Self:
        if isinstance(other, self.__class__):
            return Self(other.x // self.x, other.y // self.y, other.z // self.z)
        elif isinstance(other, self._dtype):
            return Self(other // self.x, other // self.y, other // self.z)
        else:
            return NotImplemented


class Int3(Vec3[int]):
    def __init__(self, x: int, y: int, z: int):
        super().__init__(x, y, z, dtype=int)


class Float3(Vec3[float]):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z, dtype=float)


class Bool3(Vec3[bool]):
    def __init__(self, x: bool, y: bool, z: bool):
        super().__init__(x, y, z, dtype=bool)


if __name__ == "__main__":
    # basic Vec3 tests

    i3 = Int3(1, 2, 3)
    assert i3._dtype is int

    f3 = Float3(1.0, 2, 3)
    assert f3._dtype is float

    f3 = Float3(1, 2, 3)
    assert f3._dtype is float

    print("tests passed")
