import pymysql
from pymysql.cursors import DictCursor

class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            database="shoes",
            user="root",
            password="",
            port=3308,
            host="localhost",
            cursorclass=DictCursor
        )

    def cursor(self):
        return self.conn.cursor()


    def login(self, login, password):
        with self.cursor() as cur:
            cur.execute("select * from users where password = %s and login = %s", (password, login))
        return cur.fetchone()

    def get_all_products(self, search="", quantity="По умолчанию", manufacture="Все"):

        sql = """
        select p.id, p.article, p.title, c.title as category,
               p.description, m.title as manufacture, s.title as suppiler,
               p.price, u.title as unit, p.quantity, p.discount, p.image_path as image
        from products p
        join categories c on c.id = p.category_id
        join manufactures m on m.id = p.manufacture_id
        join suppilers s on s.id = p.suppiler_id
        join units u on u.id = p.unit_id
        
        """
        params = [f'%{search}%',f'%{search}%',f'%{search}%',f'%{search}%']

        sql += " where m.title LIKE %s or c.title LIKE %s or s.title LIKE %s or p.title LIKE %s "


        if manufacture:
            sql += f' and m.title = %s'
            params.append(manufacture)

        if quantity == "По возрастанию":
            sql += " order p.quantity by asc"
        if quantity == "По убыванию":
            sql += " order p.quantity by desc"

        print(sql)
        print(params)
        with self.cursor() as cur:
            cur.execute(sql, params)
        return cur.fetchall()

    def get_all_categories(self):
        with self.cursor() as cur:
            cur.execute("select * from categories")
        return cur.fetchall()

    def get_all_manufactures(self):
        with self.cursor() as cur:
            cur.execute("select * from manufactures")
        return cur.fetchall()

    def get_all_suppilers(self):
        with self.cursor() as cur:
            cur.execute("select * from suppilers")
        return cur.fetchall()

    def get_all_units(self):
        with self.cursor() as cur:
            cur.execute("select * from units")
        return cur.fetchall()

    def add_new_product(self,article,title,category_id,description,manufacture_id,suppiler_id,price,unit_id,quantity,discount,image):
        with self.cursor() as cur:
            cur.execute("insert into products(article,title,category_id,description,manufacture_id,suppiler_id,price,unit_id,quantity,discount,image_path)"
                        "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (article,title,category_id,description,manufacture_id,suppiler_id,price,unit_id,quantity,discount,image))
            cur.connection.commit()

    def get_unit_id(self, name):
        with self.cursor() as cur:
            cur.execute("select * from units where title = %s", (name, ))
        return cur.fetchone()

    def get_suppiler_id(self,name):
        with self.cursor() as cur:
            cur.execute("select * from suppilers where title = %s", (name, ))
        return cur.fetchone()

    def get_manufacture_id(self, name):
        with self.cursor() as cur:
            cur.execute("select * from manufactures where title = %s", (name, ))
        return cur.fetchone()

    def get_category_id(self, name):
        with self.cursor() as cur:
            cur.execute("select * from categories where title = %s", (name, ))
        return cur.fetchone()

dao = Database()