from typing import Protocol, TypeVar, Generic, List

T = TypeVar("T")


class IRepository(Protocol, Generic[T]):
    def get(self, entity_id: str) -> T:
        raise NotImplementedError

    def get_all(self) -> List[T]:
        raise NotImplementedError

    def save(self, entity: T) -> None:
        raise NotImplementedError

    def update(self, entity: T) -> None:
        raise NotImplementedError

    def delete(self, entity_id: str) -> None:
        raise NotImplementedError

    def create_user_from_dict(self, user_data) -> None:
        raise NotImplementedError
