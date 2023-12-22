from psycopg2 import connect
import os


class db:
    def __init__(self):
        try:
            self.conn = connect(host='db', user=os.getenv('POSTGRES_USER'), \
                                password=os.getenv('POSTGRES_PASSWORD'), dbname=os.getenv('POSTGRES_DB'))
        except Exception as e:
            print("Не удалось подключится к ProstgreSQL.", e)

        self.conn.autocommit = True

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(open("schema.sql", "r", encoding="UTF-8").read())
        except Exception as e:
            print("Ошибка чтения .sql файла.", e)

    def get_tables_list(self) -> list:
        result = []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM information_schema.tables WHERE table_schema='public'")
                for row in cursor.fetchall():
                    result.append(row[2])
        except Exception as e:
            print("Не удалось получить список таблиц.", e)
            result = []

        return result

    def get_all_rows_from_table(self, q: str) -> list:
        result = []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(q)
                result = cursor.fetchall()
        except Exception as e:
            print("Ошибка при чтении данных.")
            result = []

        return result

    def get_headers(self, q: str):
        result = []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(f"{q} LIMIT 0")
                result = [desc[0] for desc in cursor.description]
        except Exception as e:
            print("Не удалось получить заголовки таблицы.")
            result = []

        return result

    def exec(self, query, data=list):
        # print(query)
        try:
            with self.conn.cursor() as cursor:
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                return True
        except Exception as e:
            print(e)
            return False
