import pymysql
from pymysql.cursors import DictCursor


# слой доступа к данным - все запросы к базе данных собраны здесь
class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            database="mydb",
            user="root",
            password="root",
            cursorclass=DictCursor
        )

    def cursor(self):
        return self.conn.cursor()

    def login(self, login, password):
        with self.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE login=%s AND password=%s", (login, password))
        return cur.fetchone()

    def get_all_suppliers(self):
        with self.cursor() as cur:
            cur.execute("SELECT supplier_id, supplier_name FROM suppliers")
        return cur.fetchall()

    def get_all_categories(self):
        with self.cursor() as cur:
            cur.execute("SELECT category_id, category_name FROM categories")
        return cur.fetchall()

    def get_all_manufactures(self):
        with self.cursor() as cur:
            cur.execute("SELECT manufacture_id, manufacture_name FROM manufactures")
        return cur.fetchall()

    def get_all_units(self):
        with self.cursor() as cur:
            cur.execute("SELECT unit_id, unit_name FROM units")
        return cur.fetchall()

    def get_all_statuses(self):
        with self.cursor() as cur:
            cur.execute("SELECT status_id, status_name FROM order_status")
        return cur.fetchall()

    def get_all_pickup_points(self):
        with self.cursor() as cur:
            cur.execute("SELECT pickup_point_id, address FROM pickup_points")
        return cur.fetchall()

    def get_all_users(self):
        with self.cursor() as cur:
            cur.execute("SELECT user_id, full_name FROM users")
        return cur.fetchall()

    def get_all_products(self, search="", sort="Без сортировки", supplier="Все"):
        # поиск по шести полям с опциональным фильтром по поставщику и сортировкой
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
        with self.cursor() as cur:
            cur.execute(sql, params)
        return cur.fetchall()

    def add_product(self, article, name, category_id, descrip, manufacture_id,
                    supplier_id, price, unit_id, quantity, discount, image_path):
        with self.cursor() as cur:
            cur.execute(
                """INSERT INTO products (article, product_name, category_id, descrip, manufacture_id,
                   supplier_id, price, unit_id, quantity, discount, image_path)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (article, name, category_id, descrip, manufacture_id,
                 supplier_id, price, unit_id, quantity, discount, image_path)
            )
        self.conn.commit()

    def update_product(self, product_id, article, name, category_id, descrip, manufacture_id,
                       supplier_id, price, unit_id, quantity, discount, image_path):
        with self.cursor() as cur:
            cur.execute(
                """UPDATE products SET article=%s, product_name=%s, category_id=%s, descrip=%s,
                   manufacture_id=%s, supplier_id=%s, price=%s, unit_id=%s, quantity=%s,
                   discount=%s, image_path=%s WHERE product_id=%s""",
                (article, name, category_id, descrip, manufacture_id,
                 supplier_id, price, unit_id, quantity, discount, image_path, product_id)
            )
        self.conn.commit()

    def delete_product(self, product_id):
        with self.cursor() as cur:
            cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        self.conn.commit()

    # проверяет используется ли товар в заказах перед удалением
    def product_in_orders(self, product_id):
        with self.cursor() as cur:
            cur.execute("SELECT COUNT(*) as cnt FROM orders WHERE product_id=%s", (product_id,))
            row = cur.fetchone()
        return row["cnt"] > 0

    def get_all_orders(self):
        with self.cursor() as cur:
            cur.execute("""
                SELECT o.order_id, p.article, s.status_name, pp.address,
                       o.order_date, o.delivery_date, o.product_id,
                       o.status_id, o.pickup_point_id, o.user_id
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                JOIN order_status s ON o.status_id = s.status_id
                JOIN pickup_points pp ON o.pickup_point_id = pp.pickup_point_id
            """)
        return cur.fetchall()

    def add_order(self, product_id, status_id, pickup_point_id, order_date, delivery_date, user_id):
        with self.cursor() as cur:
            cur.execute(
                """INSERT INTO orders (product_id, status_id, pickup_point_id, order_date, delivery_date, user_id)
                   VALUES (%s,%s,%s,%s,%s,%s)""",
                (product_id, status_id, pickup_point_id, order_date, delivery_date, user_id)
            )
        self.conn.commit()

    def update_order(self, order_id, product_id, status_id, pickup_point_id, order_date, delivery_date, user_id):
        with self.cursor() as cur:
            cur.execute(
                """UPDATE orders SET product_id=%s, status_id=%s, pickup_point_id=%s,
                   order_date=%s, delivery_date=%s, user_id=%s WHERE order_id=%s""",
                (product_id, status_id, pickup_point_id, order_date, delivery_date, user_id, order_id)
            )
        self.conn.commit()

    def delete_order(self, order_id):
        with self.cursor() as cur:
            cur.execute("DELETE FROM orders WHERE order_id=%s", (order_id,))
        self.conn.commit()


dao = Database()
