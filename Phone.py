import psycopg2
import Client as Client

conn = psycopg2.connect(database="postgre_sql", user="postgres", password="v12mm1997")

class Phone():
    def __init__(self, phone, id):
        self.phone = phone
        self.id = id

    def save_phone(self): # Наполнение таблицы phone
        with conn.cursor() as cur:
            cur.execute(f"""
                        INSERT INTO phone(phone_number, client_id ) VALUES (%s, %s);
                """, (self.phone, self.id))
            conn.commit()
            cur.execute("""
                    SELECT * FROM phone;
            """)
            print(cur.fetchall())  # Запрос автоматически зафиксирует изменения
        cur.close()

    def delete_phone(self):
        with conn.cursor() as cur:
            cur.execute(f"""
                        SELECT phone_id FROM phone WHERE client_id = %s AND phone_number = %s;
                """, (self.id, self.phone,))
            conn.commit()
            cur.execute("""
                    SELECT * FROM phone;
            """)
            phone_id = cur.fetchone()[0]  # Запрос автоматически зафиксирует изменения

            cur.execute(f"""
                    DELETE FROM phone WHERE phone_id = {phone_id};
            """)
            conn.commit()

        cur.close()
        print("Запись удалена")

def search_client_phone(phone):
    with conn.cursor() as cur:
        cur.execute(f"""
                            SELECT * FROM phone WHERE phone_number=%s;
                    """, (phone,))
        conn.commit()
        return cur.fetchone()
    cur.close()
