import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, reference):
        return self.session.query(model.Product).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Product).all()