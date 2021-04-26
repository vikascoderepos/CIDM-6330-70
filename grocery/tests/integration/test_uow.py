import pytest
from addition.domain import model
from addition.service_layer import unit_of_work


def insert_product(session, ref, sku, qty, maxAllowedPurchaseQty, brand, price):
    session.execute(
        "INSERT INTO products (reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand, price)"
        ' VALUES (:ref, :sku, :qty, :maxAllowedPurchaseQty, :brand, :price)',
        dict(ref=ref, sku=sku, qty=qty, maxAllowedPurchaseQty=maxAllowedPurchaseQty, brand=brand ,  price=price)
    )


def get_added_product_ref(session, itemid, sku):
    [[cartitemid]] = session.execute(
        'SELECT id FROM items WHERE itemid=:itemid AND sku=:sku',
        dict(itemid=itemid, sku=sku)
    )
    [[productref]] = session.execute(
        'SELECT p.reference FROM items JOIN products AS p ON "product_id" = p.id'
        ' WHERE "cartitem_id"=:cartitemid',
        dict(cartitemid=cartitemid)
    )
    return productref


def test_uow_can_retrieve_a_product_and_add_to_it(session_factory):
    session = session_factory()
    insert_product(session, "product1", "EASTERN-MASALA", 100, 10, "EASTERN", 1.65)
    session.commit()

    # either:
    # uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    # with uow:

    # or perhaps
    # with unit_of_work.start(session_factory) as uow: ?

    #     product = uow.products.get(reference='product1')
    #     item = model.CartItem('i1', 'EASTERN-MASALA', 10)
    #     product.add(item)
    #     uow.commit()

    productref = get_added_product_ref(session, 'i1', 'EASTERN-MASALA')
    assert productref == 'product1'


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_product(uow.session, "product1", "EASTERN-MASALA", 100, 10, "EASTERN", 1.65)

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "products"'))
    assert rows == []


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_prduct(uow.session, "product1", "EASTERN-MASALA", 100, 10, "EASTERN", 1.65)
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "products"'))
    assert rows == []
