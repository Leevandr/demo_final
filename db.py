import pymysql
from pymysql.cursors import DictCursor


class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost", database="mydb",
            user="root", password="root",
            cursorclass=DictCursor
        )

    def _fetch(self, sql, params=()):
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def _fetch_one(self, sql, params=()):
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def _execute(self, sql, params=()):
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
        self.conn.commit()

    def login(self, login, password):
        return self._fetch_one(
            "SELECT * FROM users WHERE login=%s AND password=%s", (login, password)
        )

    def get_all_suppliers(self):
        return self._fetch("SELECT supplier_id, supplier_name FROM suppliers")

    def get_all_categories(self):
        return self._fetch("SELECT category_id, category_name FROM categories")

    def get_all_manufactures(self):
        return self._fetch("SELECT manufacture_id, manufacture_name FROM manufactures")

    def get_all_units(self):
        return self._fetch("SELECT unit_id, unit_name FROM units")

    def get_all_statuses(self):
        return self._fetch("SELECT status_id, status_name FROM order_status")

    def get_all_pickup_points(self):
        return self._fetch("SELECT pickup_point_id, address FROM pickup_points")

    def get_all_users(self):
        return self._fetch("SELECT user_id, full_name FROM users")

    def get_all_products(self, search="", sort="Без сортировки", supplier="Все"):
        sql = """
            SELECT p.product_id, p.article, p.category_id, p.manufacture_id,
                   p.supplier_id, p.unit_id, category_name, product_name,
                   unit_name, quantity, manufacture_name, descrip,
                   supplier_name, discount, price, image_path
            FROM products p
            JOIN categories USING(category_id)
            JOIN units USING(unit_id)
            JOIN manufactures USING(manufacture_id)
            JOIN suppliers USING(supplier_id)
            WHERE (category_name LIKE %s OR descrip LIKE %s OR product_name LIKE %s
                   OR manufacture_name LIKE %s OR supplier_name LIKE %s OR unit_name LIKE %s)
        """
        s = f"%{search}%"
        params = [s] * 6
        if supplier != "Все":
            sql += " AND supplier_name = %s"
            params.append(supplier)
        if sort == "По возрастанию кол-ва на складе":
            sql += " ORDER BY quantity ASC"
        elif sort == "По убыванию кол-ва на складе":
            sql += " ORDER BY quantity DESC"
        return self._fetch(sql, params)

    def add_product(self, article, name, category_id, descrip, manufacture_id,
                    supplier_id, price, unit_id, quantity, discount, image_path):
        self._execute(
            """INSERT INTO products (article, product_name, category_id, descrip, manufacture_id,
               supplier_id, price, unit_id, quantity, discount, image_path)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (article, name, category_id, descrip, manufacture_id,
             supplier_id, price, unit_id, quantity, discount, image_path)
        )

    def update_product(self, product_id, article, name, category_id, descrip, manufacture_id,
                       supplier_id, price, unit_id, quantity, discount, image_path):
        self._execute(
            """UPDATE products SET article=%s, product_name=%s, category_id=%s, descrip=%s,
               manufacture_id=%s, supplier_id=%s, price=%s, unit_id=%s, quantity=%s,
               discount=%s, image_path=%s WHERE product_id=%s""",
            (article, name, category_id, descrip, manufacture_id,
             supplier_id, price, unit_id, quantity, discount, image_path, product_id)
        )

    def delete_product(self, product_id):
        self._execute("DELETE FROM products WHERE product_id=%s", (product_id,))

    def product_in_orders(self, product_id):
        row = self._fetch_one("SELECT COUNT(*) as cnt FROM orders WHERE product_id=%s", (product_id,))
        return row["cnt"] > 0

    def get_all_orders(self):
        return self._fetch("""
            SELECT o.order_id, p.article, s.status_name, pp.address,
                   o.order_date, o.delivery_date, o.product_id,
                   o.status_id, o.pickup_point_id, o.user_id
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            JOIN order_status s ON o.status_id = s.status_id
            JOIN pickup_points pp ON o.pickup_point_id = pp.pickup_point_id
        """)

    def add_order(self, product_id, status_id, pickup_point_id, order_date, delivery_date, user_id):
        self._execute(
            """INSERT INTO orders (product_id, status_id, pickup_point_id, order_date, delivery_date, user_id)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (product_id, status_id, pickup_point_id, order_date, delivery_date, user_id)
        )

    def update_order(self, order_id, product_id, status_id, pickup_point_id, order_date, delivery_date, user_id):
        self._execute(
            """UPDATE orders SET product_id=%s, status_id=%s, pickup_point_id=%s,
               order_date=%s, delivery_date=%s, user_id=%s WHERE order_id=%s""",
            (product_id, status_id, pickup_point_id, order_date, delivery_date, user_id, order_id)
        )

    def delete_order(self, order_id):
        self._execute("DELETE FROM orders WHERE order_id=%s", (order_id,))


dao = Database()
