import abc

import model
from model import Batch


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, batch) -> None:
        self.session.add(batch)

    def get(self, reference) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()


class FakeRepository(AbstractRepository):
    def __init__(self, batches) -> None:
        self._batches = batches

    def add(self, batch) -> None:
        self._batches.add(batch)

    def get(self, reference) -> Batch:
        return next(batch for batch in self._batches if batch.reference == reference)

    def list(self) -> list[Batch]:  # noqa: A003
        return list(self._batches)
