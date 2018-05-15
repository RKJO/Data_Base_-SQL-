'''
CREATE TABLE Payment(
  id serial,
  type text,
  date date,
  PRIMARY KEY(id),
  FOREIGN KEY (id)
  REFERENCES Tickets(id)
);
'''

from flask import Flask, request
from psycopg2 import connect, OperationalError


def create_connection(db_name="cinema_db"):
    username = "postgres"
    password = "coderslab"
    host = "localhost"

    try:
        connection = connect(user=username, password=password, host=host, database=db_name)
        return connection
    except OperationalError:
        return None


forms = """
    <form class="payment_form" method="post" action="#">
        <label>Typ platnosci</label><br>
        <select name="payment_type">
            <option value="transfer">Przelew</option>
            <option value="cash">Gotówka</option>
            <option value="card">Karta</option>
        </select><br>
        <label>Data</label><br>
        <input type="date" name="payment_date"><br>
        <button type="submit" name="submit" value="payment">Wyślij</button>
    </form>
    """

app = Flask('payment')


@app.route('/')
def index():
    cnx = create_connection()
    if cnx:
        cursor = cnx.cursor()
        cursor.execute('''SELECT * FROM Tickets''')
        result = '<h1>products</h1><ul>{}</ul>'
        ticket_string = ''
        for ticket in cursor:
            ticket_string += "<li>{} {} {}</li>".format(ticket[0], ticket[1], ticket[2])
        cursor.close()
        cnx.close()
        return result.format(ticket_string)
    return "No connection"


@app.route('/add_payments/<int:ticket_id>', methods=['POST', 'GET'])
def add_payments(ticket_id):
    if request.method == 'GET':
        return forms
    else:
        cnx = create_connection()
        cursor = cnx.cursor()
        payment_type = request.form['payment_type']
        date = request.form['payment_date']
        cursor.execute("""
        INSERT INTO payment(id, type, date)
        VALUES ({}, '{}', '{}')
        """.format(ticket_id, payment_type, date))
        cnx.commit()
        cursor.close()
        cnx.close()
        return "Udało się"

'''
-- Tylko opłacone gotówką
SELECT * FROM Tickets JOIN Payments
ON Tickets.id = Payments.id WHERE Payments.type = 'cash';
-- Tylko nieopłacone
SELECT * FROM Tickets LEFT JOIN Payments
ON Tickets.id = Payments.id WHERE Payments.id is null;
'''


if __name__ == '__main__':
    app.run(debug=True)