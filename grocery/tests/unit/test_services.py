import pytest
from addition.adapters import repository
from addition.service_layer import services, unit_of_work

class FakeRepository(repository.AbstractRepository):
    def __init__(self, products):
        self._products= set(products)

    def add(self, product):
        self._products.add(product)

    def get(self, reference):
        return next(p for p in self._products if p.reference == reference)

    def list(self):
        return list(self._products)

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.products = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_product():
    uow = FakeUnitOfWork()
    services.add_product("p1", "CHAKRI ATTA", 100,  100, 'CHAKRI ATTA' , 16, uow)
    assert uow.products.get("p1") is not None
    assert uow.committed




def test_returns_item():
    uow = FakeUnitOfWork()
    services.add_product("product1", "CHAKRI ATTA", 100,  100, 'CHAKRI ATTA' , 16, uow)
    result = services.add("i1", "CHAKRI ATTA", 10, uow)
    assert result == "product1"


def test_add_errors_for_invalid_sku():
    item = model.CartItem("i1", "NONEXISTENTSKU", 10)
    product = model.Product("p1", "AREALSKU", 100,  100, 'A REAL SKU' , 100)
    repo = FakeRepository([product])

    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.add(item, repo, FakeSession())


def test_commits():
    item = model.CartItem("i1", "CHAKRI ATTA", 10)
    product = model.Product("p1", "CHAKRI ATTA", 100,  100, 'CHAKRI ATTA' , 16)
    repo = FakeRepository([product])
    session = FakeSession()

    services.add(item, repo, session)
    assert session.committed is True