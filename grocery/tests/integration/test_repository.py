from addition.domain import model
from addition.adapters import repository


def test_repository_can_save_a_product(session):
    product = model.Product("product1", "PALAK-LEAF", 100, 10, "OM PRODUCES", 1.45)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(product)
    session.commit()

    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand, price FROM "products"'
    )
    assert list(rows) == [("product1", "PALAK-LEAF", 100, 10, "OM PRODUCES", 1.45)]


def insert_cart_item(session):
    session.execute(
        "INSERT INTO cart_items (itemid, sku, qty)"
        ' VALUES ("item1", "EASTERN-MASALA", 5)'
    )
    [[cartitem_id]] = session.execute(
        "SELECT id FROM cart_items WHERE itemid=:itemid AND sku=:sku",
        dict(itemid="item1", sku="EASTERN-MASALA"),
    )
    return cartitem_id


def insert_product(session, product_id):
    session.execute(
        "INSERT INTO products (reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand, price)"
        ' VALUES (:product_id, "EASTERN-MASALA", 100, 10, "EASTERN", 1.65)',
        dict(product_id=product_id),
    )
    [[product_id]] = session.execute(
        'SELECT id FROM products WHERE reference=:product_id AND sku="EASTERN-MASALA"',
        dict(product_id=product_id),
    )
    return product_id


def insert_item(session, cartitem_id, product_id):
    session.execute(
        "INSERT INTO items (cartitem_id, product_id)"
        " VALUES (:cartitem_id, :product_id)",
        dict(cartitem_id=cartitem_id, product_id=product_id),
    )


def test_repository_can_retrieve_a_product_with_items(session):
    cartitem_id = insert_cart_item(session)
    product1_id = insert_product(session, "product1")
    insert_product(session, "product2")
    insert_item(session, cartitem_id, product1_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("product1")

    expected = model.Product("product1", "EASTERN-MASALA", 100, 10, "EASTERN", 1.65)
    assert retrieved == expected  # Product.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._items == {
        model.CartItem("item1", "EASTERN-MASALA", 5),
    }