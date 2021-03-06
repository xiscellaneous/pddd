from abc import (
    abstractmethod,
    ABC,
)
from typing import (
    Type,
    List,
)

from pydantic import (
    BaseModel as PydanticModel,
)

from pddd.entities import (
    Entity,
)
from pddd.repositories import (
    Repository,
    CreateRepository,
    ReadRepository,
    UpdateRepository,
    DeleteRepository,
    CrudRepository,
)
from pddd.services import (
    Service,
    CreateService,
    ReadService,
    UpdateService,
    DeleteService,
)


class PydanticService(Service, ABC):
    @property
    @abstractmethod
    def repository(self) -> Repository:
        raise NotImplementedError()


class PydanticCreateMixin(CreateService, ABC):
    @property
    @abstractmethod
    def repository(self) -> CreateRepository:
        raise NotImplementedError()

    @property
    @abstractmethod
    def create_model(self) -> Type[PydanticModel]:
        raise NotImplementedError()

    async def create(self, inputs: dict) -> dict:
        model: PydanticModel = self.create_model(**inputs)

        kwargs: dict = model.dict()
        entity: Entity = self.repository.entity(
            **kwargs,  # noqa
        )

        new_entity = await self.repository.create(entity)
        return new_entity.__dict__


class PydanticReadMixin(ReadService, ABC):
    @property
    @abstractmethod
    def repository(self) -> ReadRepository:
        raise NotImplementedError()

    @property
    @abstractmethod
    def read_model(self) -> Type[PydanticModel]:
        raise NotImplementedError()

    async def read(self, filters: dict) -> List[dict]:
        model: PydanticModel = self.read_model(**filters)

        entities: list = await self.repository.read(filters=model.dict())

        return [
            entity.__dict__
            for entity in entities
        ]


class PydanticUpdateMixin(UpdateService, ABC):
    @property
    @abstractmethod
    def repository(self) -> UpdateRepository:
        raise NotImplementedError()

    @property
    @abstractmethod
    def update_model(self) -> Type[PydanticModel]:
        raise NotImplementedError()

    async def update(self, id_: str, inputs: dict) -> dict:
        model: PydanticModel = self.update_model(id=id_, **inputs)

        kwargs: dict = model.dict()
        entity: Entity = self.repository.entity(
            **kwargs,  # noqa
        )

        new_entity = await self.repository.update(entity)
        return new_entity.__dict__


class PydanticDeleteMixin(DeleteService, ABC):
    @property
    @abstractmethod
    def repository(self) -> DeleteRepository:
        raise NotImplementedError()

    @property
    @abstractmethod
    def delete_model(self) -> Type[PydanticModel]:
        raise NotImplementedError()

    async def delete(self, id_: str) -> None:
        model: PydanticModel = self.delete_model(id=id_)

        kwargs: dict = model.dict()
        entity: Entity = self.repository.entity(
            **kwargs,  # noqa
        )

        await self.repository.delete(entity)


class PydanticCrudService(
    PydanticService,
    PydanticCreateMixin,
    PydanticReadMixin,
    PydanticUpdateMixin,
    PydanticDeleteMixin,
    ABC,
):
    @property
    @abstractmethod
    def repository(self) -> CrudRepository:
        raise NotImplementedError()
