import psycopg2

def create_tables(cur):   
   
    cur.execute("""
        DROP TABLE if exists phone;
        DROP TABLE if exists client;                
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


def update_client(cur, id, new_name=None, new_surname=None, new_mail=None):
    def d_dict():
         return {'name': new_name, 'surname': new_surname, 'mail': new_mail}
    
    dc_dict = d_dict()

    data_dict = {}

    for key in dc_dict:
        
        if dc_dict[key] != None:
            data_dict[key] = dc_dict[key]


    data_list = []
    for key in data_dict:
        data_list.append((key + ' = %(' + key + ')s'))

    data_st = 'UPDATE client SET ' + ' AND '.join(data_list) + 'WHERE id=%(id)s;'

    data_dict['id'] = id

    cur.execute(data_st, data_dict)

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

    def d_dict():
         return {'name': name, 'surname': surname, 'mail': mail, 'phone': phone}
    
    dc_dict = d_dict()

    data_dict = {}

    for key in dc_dict:
        
        if dc_dict[key] != None:
            data_dict[key] = dc_dict[key]


    data_list = []
    for key in data_dict:
        data_list.append((key + ' = %(' + key + ')s'))

    data_st = 'SELECT c.id, c.name, c.surname, p.phone FROM client c JOIN phone p on c.id = p.client_id WHERE ' + ' AND '.join(data_list) + ';'

    cur.execute(data_st, data_dict)
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

            phones = [(1, '+6530769'), (3, '+03498794944')]
            for i in phones:
                add_phone(cur, i[0], i[1])
        
            print(find_client(cur, surname='Smith', mail='anna@smith.com'))
            id_1 = find_client(cur, surname='Smith')[0][0]
            add_phone(cur, id_1, '+3979657463')

            print(find_client(cur, name='Tom', phone='+03472888834'))
            id_2 =find_client(cur, phone='+03472888834')[0][0]
            add_phone(cur, id_2, '+70997867556')

            update_client(cur, 2, new_mail='snak@hgh.com')

            delete_phone(cur, 3, '+03472888834')

            delete_client(cur, 2)





