import psycopg2
import Phone as Phone

conn = psycopg2.connect(database="postgre_sql", user="postgres", password="v12mm1997")


class Client:
    def __init__(self, first_name, last_name, email): # Инициализация переменных
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def save_new_client(self): # добавление клиента в таблицу клиент
        with conn.cursor() as cur:
            cur.execute(f"""
                        INSERT INTO client(first_name, last_name, email) VALUES (%s, %s, %s);
                """, (self.first_name, self.last_name, self.email))
            conn.commit()
            cur.execute("""
                    SELECT * FROM client;
            """)
            print(cur.fetchall())  # Запрос автоматически зафиксирует изменения
        cur.close()

    def id_client(self):
        with conn.cursor() as cur:
            cur.execute(f"""
                        SELECT client_id FROM client WHERE first_name = %s AND last_name = %s AND email = %s;
                """, (self.first_name, self.last_name, self.email,))
            conn.commit()
            return cur.fetchone()[0] # Запрос автоматически зафиксирует изменения
        cur.close()

    def change(self, id):
        self.id = id
        print("Введите новое имя клиента")
        first_name = input()
        print("Введите новую фамилию клиента")
        last_name = input()
        print("Введите новый email")
        email = input()
        with conn.cursor() as cur:
            cur.execute("""
                    UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
            """, (first_name, last_name, email, self.id))
            cur.execute("""
                        SELECT * FROM client;
                """)
            conn.commit()
            print(cur.fetchall())
        print("Данные изменены")
        cur.close()

    def delete_client(self, id):
        with conn.cursor() as cur:
            cur.execute(f"""
                                DELETE FROM phone WHERE client_id = {id};
                        """)
            conn.commit()

            cur.execute(f"""
                    DELETE FROM client WHERE client_id = {id};
            """)
            conn.commit()
        cur.close()

    def search_client(self, id):
        with conn.cursor() as cur:
            cur.execute(f"""
                    SELECT first_name, last_name, email from client WHERE client_id=%s AND first_name=%s AND last_name=%s AND email=%s;
            """, (id, self.first_name, self.last_name, self.email,))
            client = cur.fetchone()
            print('Данные клиента: ', )
            print('Имя : ', client[0])
            print('Фамилия: ', client[1])
            print('Email: ', client[2])
            conn.commit()
            cur.execute("""
                    SELECT phone_number FROM phone WHERE client_id=%s;
            """, (id, ))
            conn.commit()
            print('Номер(-a) его телефонa(-ов): ')  # Извлечь все строки
            for i in cur.fetchall():
                print(i[0])
        cur.close()

def search_client_id(id):
    with conn.cursor() as cur:
        cur.execute(f"""
                            SELECT * FROM client WHERE client_id=%s;
                    """, (id,))
        conn.commit()
        return cur.fetchone()
    cur.close()



