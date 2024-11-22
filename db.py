import psycopg2
from prettytable import PrettyTable

# Параметри підключення
conn = psycopg2.connect(
    dbname="project_db", user="user", password="password", host="localhost", port="5432"
)

cursor = conn.cursor()


# Створення таблиць
def create_tables():
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Errors (
        error_id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        received_date DATE NOT NULL,
        error_level TEXT CHECK (error_level IN ('Критична', 'Важлива', 'Незначна')) NOT NULL,
        category TEXT CHECK (category IN ('Інтерфейс', 'Дані', 'Розрахунковий алгоритм', 'Інше', 'Невідома категорія')) NOT NULL,
        source TEXT CHECK (source IN ('Користувач', 'Тестувальник')) NOT NULL
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Programmers (
        programmer_id SERIAL PRIMARY KEY,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        phone TEXT CHECK (phone ~ '^[0-9]{3}-[0-9]{3}-[0-9]{4}$') NOT NULL
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Fixes (
        fix_id SERIAL PRIMARY KEY,
        error_id INTEGER REFERENCES Errors(error_id) ON DELETE CASCADE,
        start_date DATE NOT NULL,
        duration INTEGER CHECK (duration IN (1, 2, 3)) NOT NULL,
        programmer_id INTEGER REFERENCES Programmers(programmer_id) ON DELETE CASCADE,
        daily_rate NUMERIC NOT NULL CHECK (daily_rate > 0)
    );
    """
    )

    conn.commit()
    print("Таблиці створено.")


def insert_data():
    errors = [
        ("Опис помилки 1", "2024-11-10", "Критична", "Інтерфейс", "Користувач"),
        ("Опис помилки 2", "2024-11-12", "Важлива", "Дані", "Тестувальник"),
        # Додайте ще 18 записів
    ]
    programmers = [
        ("Іванов", "Іван", "123-456-7890"),
        ("Петренко", "Петро", "234-567-8901"),
        # Додайте ще 2 програмістів
    ]
    fixes = [
        (1, "2024-11-14", 2, 1, 150.0),
        (2, "2024-11-15", 3, 2, 200.0),
        # Додайте більше записів
    ]

    cursor.executemany(
        "INSERT INTO Errors (description, received_date, error_level, category, source) VALUES (%s, %s, %s, %s, %s);",
        errors,
    )
    cursor.executemany(
        "INSERT INTO Programmers (last_name, first_name, phone) VALUES (%s, %s, %s);",
        programmers,
    )
    cursor.executemany(
        "INSERT INTO Fixes (error_id, start_date, duration, programmer_id, daily_rate) VALUES (%s, %s, %s, %s, %s);",
        fixes,
    )

    conn.commit()
    print("Дані успішно додано.")


def print_table(description, rows):
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]
    for row in rows:
        table.add_row(row)
    print(table)


def print_all_tables():
    tables = ["Errors", "Fixes", "Programmers"]

    for i in tables:
        cursor.execute(f"""SELECT * FROM {i}""")
        print(f"Таблиця {i}")
        print(print_table(cursor.description, cursor.fetchall()))
