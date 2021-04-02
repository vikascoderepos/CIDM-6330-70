import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Bookmark):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Bookmark:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> model.Bookmark:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, bookmark):
        self.session.add(bookmark)

    def get(self, id):
        return self.session.query(model.Bookmark).filter_by(id=id).one()

    def list(self):
        return self.session.query(model.Bookmark).all()

