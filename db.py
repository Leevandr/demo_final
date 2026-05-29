import pymysql
from pymysql.cursors import DictCursor


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
            cur.execute("select * from users where login = %s and password = %s", (login, password))
        return cur.fetchone()

    def get_all_postav(self):
        with self.cursor() as cur:
            cur.execute("select supplier_name from suppliers")
        return cur.fetchall()

    def get_all_products(self, search="", sort="Без сортировки", supplier="Все"):
        sql = """
            SELECT 
                category_name, 
                product_name, 
                unit_name, 
                quantity, 
                manufacture_name, 
                descrip, 
                supplier_name, 
                discount, 
                price,
                image_path
            FROM products
            JOIN categories USING(category_id)
            JOIN units USING(unit_id)
            JOIN manufactures USING(manufacture_id)
            JOIN suppliers USING(supplier_id)
            where (category_name like %s 
                or descrip like %s
                or product_name like %s
                or manufacture_name like %s) \
        """

        search_param = f"%{search}%"
        params = [search_param, search_param, search_param, search_param]


        if supplier != "Все":
            sql += "and supplier_name  = %s"
            params.append(supplier)

        if sort == "По возрастанию кол-ва на складе":
            sql += " order by quantity asc"

        if sort == "По убыванию кол-ва на складе":
            sql += " order by quantity desc"

        with self.cursor() as cur:
            cur.execute(sql, params)
        return cur.fetchall()

dao = Database()