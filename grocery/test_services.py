import pytest
import model
import repository
import services


class FakeRepository(repository.AbstractRepository):
    def __init__(self, products):
        self._products= set(products)

    def add(self, product):
        self._products.add(product)

    def get(self, reference):
        return next(p for p in self._products if p.reference == reference)

    def list(self):
        return list(self._products)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_returns_item():
    item = model.CartItem("i1", "CHAKRI ATTA", 10)
    product = model.Product("p1", "CHAKRI ATTA", 100,  100, 'CHAKRI ATTA' , 16)
    repo = FakeRepository([product])

    result = services.add(item, repo, FakeSession())
    assert result == "p1"


def test_error_for_invalid_sku():
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