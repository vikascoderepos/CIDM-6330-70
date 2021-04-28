from addition.domain import model


def test_cartitem_mapper_can_load_items(session):
    session.execute(
        "INSERT INTO cart_items (itemid, sku, qty) VALUES "
        '("item1", "AMUL-GHEE", 2),'
        '("item2", "KAVAN-CHAPATHI", 5),'
        '("item3", "MURUKU-SNAKCS", 6)'
    )
    expected = [
        model.CartItem("item1", "AMUL-GHEE", 2),
        model.CartItem("item2", "KAVAN-CHAPATHI", 5),
        model.CartItem("item3", "MURUKU-SNAKCS", 6),
    ]
    assert session.query(model.CartItem).all() == expected


def test_cartitem_mapper_can_save_items(session):
    new_item = model.CartItem("item1", "KASHMIRI-CHILLY", 2)
    session.add(new_item)
    session.commit()

    rows = list(session.execute('SELECT itemid, sku, qty FROM "cart_items"'))
    assert rows == [("item1", "KASHMIRI-CHILLY", 2)]


def test_retrieving_products(session):
    session.execute(
        "INSERT INTO products (reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand , price)"
        ' VALUES ("product1", "sku1", 100, 10, "IDAYAM", 5.65 )'
    )
    session.execute(
        "INSERT INTO products (reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand , price)"
        ' VALUES ("product2", "sku2", 200, 5, "MAGGI", 1.25)'
    )
    expected = [
        model.Product("product1", "sku1", 100, 10, "IDAYAM", 5.65),
        model.Product("product2", "sku2", 200, 5, "MAGGI", 1.25),
    ]

    assert session.query(model.Product).all() == expected


def test_saving_products(session):
    product = model.Product("product1", "sku1", 100,  10, "IDAYAM", 5.65)
    session.add(product)
    session.commit()
    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand, price FROM "products"'
    )
    assert list(rows) == [("product1", "sku1", 100, 10, "IDAYAM", 5.65)]


def test_saving_items(session):
    product = model.Product("product1", "sku1", 100, 10, "IDAYAM", 5.65)
    item = model.CartItem("item1", "sku1", 2)
    product.add(item)
    session.add(product)
    session.commit()
    rows = list(session.execute('SELECT cartitem_id, product_id FROM "items"'))
    assert rows == [(product.id, item.id)]


def test_retrieving_items(session):
    session.execute(
        'INSERT INTO cart_items (itemid, sku, qty) VALUES ("item1", "sku1", 12)'
    )
    [[ciid]] = session.execute(
        "SELECT id FROM cart_items WHERE itemid=:itemid AND sku=:sku",
        dict(itemid="item1", sku="sku1"),
    )
    session.execute(
        "INSERT INTO products (reference, sku, _purchased_quantity, maxAllowedPurchaseQty, brand, price)"
        ' VALUES ("product1", "sku1", 100, 10, "IDAYAM", 5.65)'
    )
    [[pid]] = session.execute(
        "SELECT id FROM products WHERE reference=:ref AND sku=:sku",
        dict(ref="product1", sku="sku1"),
    )
    session.execute(
        "INSERT INTO items (cartitem_id, product_id) VALUES (:ciid, :pid)",
        dict(ciid=ciid, pid=pid),
    )

    product = session.query(model.Product).one()

    assert product._items == {model.CartItem("item1", "sku1", 12)}