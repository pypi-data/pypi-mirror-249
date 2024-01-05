"""Module of `Undefined` and `UndefinedType` classes."""
__all__ = ("Undefined", "UndefinedType")

from typing import final, Optional, TYPE_CHECKING

from typing_extensions import TypeAlias


class UndefinedMeta(type):
    """Metaclass to define behavior of `UndefinedType`."""

    __instance__: Optional["UndefinedType"] = None

    def __call__(cls, *_args, **_kwargs) -> "UndefinedType":
        if cls.__instance__ is None:
            cls.__instance__ = super().__call__("Undefined", (), {})

        return cls.__instance__


@final
class UndefinedType(type, metaclass=UndefinedMeta):
    """Represents Undefined constant."""

    def __bool__(self):
        """Represent UndefinedType as boolean."""
        return False

    def __str__(self) -> str:
        """Represent UndefinedType as string."""
        return "Undefined"

    def __repr__(self) -> str:
        """Represent UndefinedType."""
        return "Undefined"


if TYPE_CHECKING:
    Undefined: TypeAlias = type
else:
    Undefined = UndefinedType("Undefined")
