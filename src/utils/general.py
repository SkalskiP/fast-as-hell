from typing import Optional, TypeVar

T = TypeVar('T')


def exists(item: Optional[T]) -> bool:
    return item is not None


def get_or_else(item: Optional[T], default: T) -> T:
    return item if exists(item) else default
