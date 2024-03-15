import psycopg2
import Client as Client
import Phone as Phone

# Подключаемся параметрами к базе данных
conn = psycopg2.connect(database="postgre_sql", user="postgres", password="v12mm1997")

HELP = """
    Команды программы:
    CREATE_TABLE  - Функция, создающая структуру БД (таблицы).
    ADD_client    - Функция, позволяющая добавить нового клиента.
    ADD_phone     - Функция, позволяющая добавить телефон для существующего клиента.
    CHANGE_Client - Функция, позволяющая изменить данные о клиенте.
    DELETE_PHONE  - Функция, позволяющая удалить номер телефона клиента. 
    DELETE_CLIENT - Функция, позволяющая удалить существующего клиента.
    SEARCH_CLIENT - Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
    CLEAR_ALL     - Очистить все данные о пользователях и номера телефонов
    DROP_TABLE    - Удалить все таблицы
    EXIT          - Выход
"""


# Открываем базу данных и создаем таблицы c клиентом

def create_table():
    with conn.cursor() as cur:
        cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS client(
                           client_id SERIAL PRIMARY KEY,
                           first_name VARCHAR(40) NOT NULL ,
                           last_name VARCHAR(40) NOT NULL,
                           email VARCHAR(40) NOT NULL
                           );
                    """)
        cur.execute(f"""
                            CREATE TABLE IF NOT EXISTS phone(
                            phone_id SERIAL PRIMARY KEY,
                            client_id INTEGER NOT NULL REFERENCES client(client_id),
                            phone_number VARCHAR(40)
                            );
                            """)
        conn.commit() # Фисксируем в БД
    cur.close()
    print("Таблицы созданы")


 # Coздали таблицу для клиента и для телефонов

def clear_data():
    with conn.cursor() as cur:
        cur.execute(f"""
                            DELETE FROM phone;
                            """)
        conn.commit()
        cur.execute(f"""
                            DELETE FROM client;
                            """)
        conn.commit()
    cur.close()

def clear_table():
    with conn.cursor() as cur:
        cur.execute(f"""
                            DROP TABLE phone;
                            """)
        conn.commit()
        cur.execute(f"""
                            DROP TABLE client;
                            """)
        conn.commit()
    cur.close()

while True: # Структура программы
    print(HELP)
    print("Введите команду: ")
    command = input()
    if command == 'ADD_client':  # Добавление нового клиента
        print("Введите имя клиента : ")
        first_name = input()
        print("Введите фамилию : ")
        last_name = input()
        print("Введите email: ")
        email = input()
        client = Client.Client(first_name, last_name, email)
        client.save_new_client() # Добавили клиента
        print("Клиент добавлен")

    elif command == "ADD_phone":
        print("Введите имя клиента : ")
        first_name = input()
        print("Введите фамилию : ")
        last_name = input()
        print("Введите email: ")
        email = input()
        print("Введите телефон клиента: ")
        phone = input()
        id = Client.Client(first_name, last_name, email).id_client() # Получаем id клиента, чтобы записать его id в таблицу phone
        print(id)
        phone_number = Phone.Phone(phone, id)
        phone_number.save_phone() # сохраняем телефон

    elif command == "CHANGE_Client":
        print("Введите имя клиента : ")
        first_name = input()
        print("Введите фамилию : ")
        last_name = input()
        print("Введите email: ")
        email = input()
        id_client = Client.Client(first_name, last_name, email)
        id = id_client.id_client()
        id_client.change(id) # Данные клиента Изменены

    elif command == "DELETE_PHONE":
        print("Введите имя клиента : ")
        first_name = input()
        print("Введите фамилию : ")
        last_name = input()
        print("Введите email: ")
        email = input()
        print("Введите телефон, который нужно удалить")
        phone = input()
        id_client = Client.Client(first_name, last_name, email)
        id = id_client.id_client()
        phone_client = Phone.Phone(phone, id)
        phone_client.delete_phone()

    elif command == "DELETE_CLIENT":
        print("Введите имя клиента : ")
        first_name = input()
        print("Введите фамилию : ")
        last_name = input()
        print("Введите email: ")
        email = input()
        id_client = Client.Client(first_name, last_name, email)
        id = id_client.id_client()
        id_client.delete_client(id)

    elif command == "SEARCH_CLIENT":
        print("Как искать клиента ? По имени, фамилии, email или по телефону? ")
        print("Введите 1 -  по имени, фамилии, email")
        print("Введите 2 - по телефону")
        com_search = int(input())
        if com_search == 1:
            print("Введите имя клиента : ")
            first_name = "Михаил"
            print("Введите фамилию : ")
            last_name = "Терентьев"
            print("Введите email: ")
            email = "terentev@mail.ru"
            client = Client.Client(first_name, last_name, email)
            id = client.id_client()
            client.search_client(id)

        elif com_search == 2:
            print("Введите номер телефона клиента: ")
            phone_search = input()
            # Узнаем id клиента по номеру телефона
            id_client = Phone.search_client_phone(phone_search)
            print("Имя: ", Client.search_client_id(id_client[1])[1]) # Узнаем все данные по id клиента
            print("Фамилия: ", Client.search_client_id(id_client[1])[2])
            print("Email: ", Client.search_client_id(id_client[1])[3])
            with conn.cursor() as cur:
                cur.execute("""
                                    SELECT phone_number FROM phone WHERE client_id=%s;
                            """, (id_client[1],))
                conn.commit()
                print('Номер(-a) его телефонa(-ов): ')  # Извлечь все строки
                for i in cur.fetchall():
                    print(i[0])
            cur.close()

    elif command == 'CREATE_TABLE':
        create_table()
        print("Таблицы созданы")

    elif command == "CLEAR_ALL":
        clear_data()
        print("Данные очищены")

    elif command == "DROP_TABLE":
        clear_table()
        print("Таблицы удалены")

    elif command == "EXIT":
        break

    else:
        continue









