"""
ALTER TABLE "order" ADD PRIMARY KEY(id);
CREATE TABLE order_product(
	id serial,
	order_id int not null,
	product_id int not null,
	PRIMARY KEY (id),
	FOREIGN KEY (order_id)
	REFERENCES "order" (id),
	FOREIGN KEY (product_id)
	REFERENCES Product(id)
);
INSERT INTO order_product(order_id,product_id)
VALUES (1, 3),
(1,2),
(2,1),
(2,3),
(3,3);
SELECT * FROM "order";
SELECT * FROM product
JOIN order_product ON product.id = order_product.product_id
WHERE order_product.order_id = 1;

SELECT * FROM product;

SELECT "order".id, description FROM "order"
JOIN order_product ON "order".id = order_product.order_id
WHERE order_product.product_id = 3;
"""

from flask import Flask
from psycopg2 import connect, OperationalError


def create_connection(db_name="exercise_db"):
    username = "postgres"
    password = "coderslab"
    host = "localhost"

    try:
        connection = connect(user=username, password=password, host=host, dbname=db_name)
        return connection
    except OperationalError:
        return None


app = Flask("tickets")


@app.route("/")
def index():
    cnx = create_connection()
    if cnx:
        result_string = ""
        cursor = cnx.cursor()
        cursor.execute("""
             SELECT id, description FROM "order";
         """)
        # Używamy fetchall, ponieważ nie możemy skorzystać z cursora
        # Do wykonania kolejnego zapytania dopuki go nie opróźnimy
        for order in cursor.fetchall():
            result_string += "Zamówienie: {} {}<br>".format(order[0], order[1])
            cursor.execute("""
             SELECT name, description, price FROM product 
             JOIN order_product ON product.id = order_product.product_id
             WHERE order_product.order_id = {};
             """.format(order[0]))
            for product in cursor:
                result_string += "Produkt: {} {} {}<br>".format(product[0], product[1], product[2])
            cursor.close()
        cnx.close()
        return result_string
    return "Nie ma bazy :("


@app.route('/products')
def products():
    cnx = create_connection()
    if cnx:
        result_string = ""
        cursor = cnx.cursor()
        cursor.execute("""
             SELECT id, name, price FROM product;
         """)
        # Używamy fetchall, ponieważ nie możemy skorzystać z cursora
        # Do wykonania kolejnego zapytania dopuki go nie opróźnimy
        for product in cursor.fetchall():
            result_string += "Produkt: {} {} {}<br>".format(
                product[0], product[1], product[2]
            )
            cursor.execute("""
                 SELECT "order".id, description FROM "order" 
                 JOIN order_product ON "order".id = order_product.order_id
                 WHERE order_product.product_id = {};
             """.format(product[0]))
            for order in cursor:
                result_string += "-----Zamowienie: {} {}<br>".format(order[0], order[1])
            cursor.close()
        cnx.close()
        return result_string
    return "Nie ma bazy :("


if __name__ == "__main__":
    app.run(debug=True)