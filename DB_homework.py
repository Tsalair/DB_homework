import psycopg2

def create_tables(cur):   
   
    cur.execute("""
        DROP TABLE if exists client;
        DROP TABLE if exists phone;                
    """)

    cur.execute("""
        CREATE TABLE client(id SERIAL PRIMARY KEY, name VARCHAR(40) not null, surname VARCHAR(60) not null, mail VARCHAR(60) not null);
        CREATE TABLE phone(id SERIAL PRIMARY KEY, client_id SERIAL references client(id), phone VARCHAR(20) unique default null);
    """)
    print('Tables client, phone created')


def add_client(cur, name, surname, mail, phone):
    cur.execute("""
        INSERT INTO client(name, surname, mail) values(%s, %s, %s) RETURNING id;
    """, (name, surname, mail))
    (id,) = cur.fetchone()

    cur.execute("""
        INSERT INTO phone(client_id, phone) values(%s, %s)
    """, (id, phone))

    print(f'Client {name} {surname} added' )


def add_phone(cur, id, phone):
 
    cur.execute("""
        SELECT phone FROM phone WHERE client_id=%s;
    """,(id,))
    (existent_phone,) = cur.fetchone()

    if existent_phone=='null':
        cur.execute("""
            UPDATE phone SET phone=%s WHERE client_id=%s;
        """, (phone, id))

    else:
        cur. execute("""
            INSERT INTO phone(client_id, phone) VALUES(%s, %s);
        """, (id, phone))

    print(f'Phone {phone} added')


def update_client(cur, id, new_name, new_surname, new_mail):
    cur.execute("""
        UPDATE client SET name=%s, surname=%s, mail=%s WHERE id=%s;
    """, (new_name, new_surname, new_mail, id))
    print('Updated')


def delete_phone(cur, id, phone):
    cur.execute("""
        DELETE FROM phone WHERE client_id=%s and phone=%s
    """, (id, phone))
    print('Phone deleted')


def delete_client(cur, id):
    cur.execute("""
        DELETE FROM phone WHERE client_id=%(cl_id)s;
        DELETE FROM client WHERE id=%(id)s;
    """, {
        'cl_id': id,
        'id': id
    })
    print('Client deleted')


def find_client(cur, name=None, surname=None, mail=None, phone=None):
    if name != None:
        cur.execute("""
            SELECT c.id, c.name, c.surname, p.phone FROM client c
            JOIN phone p on c.id = p.client_id
            WHERE c.name=%s;
        """,(name,))
        return cur.fetchall()

    elif surname != None:
        cur.execute("""
            SELECT c.id, c.name, c.surname, p.phone FROM client c
            JOIN phone p on c.id = p.client_id
            WHERE c.surname=%s;
        """,(surname,))
        return cur.fetchall()

    elif mail != None:
        cur.execute("""
            SELECT c.id, c.name, c.surname, p.phone FROM client c
            JOIN phone p on c.id = p.client_id
            WHERE c.mail=%s;
        """,(mail,))
        return cur.fetchall()

    elif phone != None:
        cur.execute("""
            SELECT c.id, c.name, c.surname, p.phone FROM client c
            JOIN phone p on c.id = p.client_id
            WHERE p.phone=%s;
        """,(phone,))
        return cur.fetchall()



if __name__ == "__main__":
    user = input('Введите user: ')
    password = input('Введите password: ')
                        
    with psycopg2.connect(dbname='client_db', user=user, password=password) as conn:
        with conn.cursor() as cur:
            create_tables(cur)

            clients = [('Anna', 'Smith', 'anna@smith.com', 'null'), 
                       ('Nikola', 'Dublew', 'dnaw@gmail.com', '+63956839'), 
                       ('Tom', 'Skillton', 'skillton@fdgh.com', '+03472888834')
                       ]
            for i in clients:
                add_client(cur, i[0], i[1], i[2], i[3])

            phones = [('Anna', 'Smith', '+6530769'), ('Tom', 'Skillton', '+03498794944')]
            for i in phones:
                add_phone(cur, i[0], i[1], i[2])
        
            print(find_client(cur, surname='Smith'))
            id_1 = find_client(cur, surname='Smith')[0][0]
            add_phone(cur, id_1, '+3979657463')

            print(find_client(cur, phone='+03472888834'))
            id_2 =find_client(cur, phone='+03472888834')[0][0]
            add_phone(cur, id_2, '+70997867556')

            update_client(cur, 2, 'Nikola', 'Dublew', 'snak@hgh.com')

            delete_phone(cur, 3, '+03472888834')

            delete_client(cur, 2)





