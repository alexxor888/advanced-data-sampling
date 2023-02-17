import psycopg2


def delete_db(conn):
    cur.execute("""
        DROP TABLE customer_phone;
        DROP TABLE customer;
        """)


def create_db(conn):
    cur.execute('CREATE TABLE IF NOT EXISTS customer ('
                'id SERIAL PRIMARY KEY, '
                'name VARCHAR (40) NOT NULL ,'
                'surname VARCHAR (40) NOT NULL,'
                'email VARCHAR (40) NOT NULL,'
                'phone VARCHAR(40));')
    cur.execute('CREATE TABLE IF NOT EXISTS customer_phone('
                'id SERIAL PRIMARY KEY,'
                'customer_id integer references customer(id),'
                'phone_number VARCHAR(180));')


def add_client(conn, first_name, last_name, email, phones):
    cur.execute("""
                   INSERT INTO customer(name, surname, email) VALUES(%s, %s, %s) 
                   RETURNING id, name, surname, email;
        """, (first_name, last_name, email))
    print(cur.fetchall())

    cur.execute("""
                    INSERT INTO customer_phone(customer_id,phone_number) VALUES(%s,%s)
                    RETURNING id, customer_id, phone_number;""", (1, phones))
    print(cur.fetchall())


def add_phone(conn, client_id, phone):
    cur.execute("""
        INSERT INTO customer_phone(phone_number, customer_id) VALUES(%s, %s);
        """, (phone, client_id))
    cur.execute("""
              SELECT * FROM customer_phone;
              """)
    print(cur.fetchall())


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
               UPDATE customer SET name=%s WHERE id=%s;
               """, (first_name, client_id))
    cur.execute("""
               UPDATE customer SET surname=%s WHERE id=%s;
               """, (last_name, client_id))
    cur.execute(f"""
               UPDATE customer SET email=%s WHERE id=%s;
               """, (email, client_id))
    cur.execute("""
               SELECT * FROM customer;
               """)
    print(cur.fetchall())
    cur.execute("""
               UPDATE customer_phone SET phone_number=%s WHERE id=%s;
               """, (phone, client_id))
    cur.execute("""
               SELECT * FROM customer_phone;
               """)
    print(cur.fetchall())


def delete_phone(conn, phone):
    cur.execute("""
        DELETE FROM customer_phone WHERE phone_number=%s;
        """, (phone,))
    cur.execute("""
        SELECT * FROM customer_phone;
        """)
    print(cur.fetchall())


def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM customer_phone WHERE customer_id=%s;
        """, (client_id,))
    cur.execute("""
        SELECT * FROM customer_phone;
        """)
    print(cur.fetchall())
    cur.execute("""
        DELETE FROM customer WHERE id=%s;
        """, (client_id,))
    cur.execute("""
        SELECT * FROM customer;
        """)
    print(cur.fetchall())


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
            SELECT id FROM customer WHERE name=%s and surname=%s and email=%s;
            """, (first_name, last_name, email,))
    print(cur.fetchone())
    cur.execute("""
            SELECT customer_id FROM customer_phone WHERE phone_number=%s;
                    """, (phone,))
    print(cur.fetchall())


if __name__ == '__main__':
    with psycopg2.connect(database="netology_db", user="postgres", password="513513") as conn:
        with conn.cursor() as cur:
            # delete_db(conn)
            # create_db(conn)
            # add_client(conn, 'Alex', 'Vitorgan', 'avitorgan@gmail.com', '+7-123-456-78-99')
            # add_phone(conn, 1, '+75555555555')
            # change_client(conn, 1, 'Kate', 'Orlova', 'orlova@mail.ru', '+72222222')
            #delete_phone(conn, '+75555555555')
            # # delete_client(conn, 1)
            # find_client(conn, 'Kate', 'Orlova', 'orlova@mail.ru', '+72222222')
    conn.close()