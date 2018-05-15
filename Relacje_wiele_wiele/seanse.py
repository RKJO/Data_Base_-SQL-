"""
CREATE TABLE seans(
	id serial,
	movies_id int not null,
	cinemas_id int not null,
	PRIMARY KEY (id),
	FOREIGN KEY (movies_id)
	REFERENCES movies (id),
	FOREIGN KEY (cinemas_id)
	REFERENCES cinemas(id)
);

INSERT INTO seans (movies_id, cinemas_id)
VALUES (1, 1)
"""

from flask import Flask, request
from psycopg2 import connect, OperationalError


app = Flask("sease")


def create_connection(db_name = "cinema_db"):
    username = "postgres"
    password = "coderslab"
    host = "localhost"

    try:
        connection = connect(user=username, password=password, host=host, dbname=db_name)
        return connection
    except OperationalError:
        return None


@app.route('/', methods=['POST', 'GET'])
def seanse():
    forms = """
    <form class="seanse" method="post" action="#">
        <label>Film</label><br>
        <select name="movies_id">
            {}
        </select><br>
        <label>Kino</label><br>
        <select name="cinemas_id">
            {}
        </select><br>
        <button type="submit" name="submit" value="payment">Wyślij</button>
    </form>
    """
    if request.method == 'GET':
        cnx = create_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT id, name FROM movies")
        option_movie = ""
        for movie in cursor:
            option_movie += "<option value='{}'>{}</option>".format(movie[0], movie[1])
        option_cinema = ""
        cursor.execute("SELECT id, name FROM cinemas")
        for cinema in cursor:
            option_cinema += "<option value='{}'>{}</option>".format(cinema[0], cinema[1])
        cursor.close()
        cnx.close()
        return forms.format(option_movie, option_cinema)
    else:
        cnx = create_connection()
        cursor = cnx.cursor()
        cinemas_id = request.form['cinemas_id']
        movies_id = request.form['movies_id']
        cursor.execute("""
            insert INTO show (cinemas_id, movies_id)
            VALUES ({},{})
        """.format(cinemas_id, movies_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return "Udało się"

''' 
SELECT * FROM cinemas
JOIN seans ON cinemas.id = seans.cinemas_id
WHERE seans.movies_id = 1

'''


@app.route('/movie/<int:movies_id>')
def movies_id():
    statment = '''
    SELECT cinemas.id, name FROM cinemas
    JOIN seans ON cinemas.id = seans.cinemas_id
    WHERE seans.movies_id = %s
    '''

    cnx = create_connection()
    cursor = cnx.cursor()
    cursor.execute(statment, (movies_id,))
    cinema_string = ''
    for cinema in cursor:
        cinema_string += "{} {} <br>".format(cinema[0], cinema[1])
    cursor.close()
    cnx.close()
    return cinema_string


if __name__ == '__main__':
    app.run(debug=True)