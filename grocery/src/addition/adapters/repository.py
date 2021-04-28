import abc
from addition.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, cart: model.Cart):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, sku) -> model.Cart:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
    def add(self, cart):

        self.session.add(cart)

    def get(self, sku):
        return self.session.query(model.Cart).filter_by(sku=sku).first()
