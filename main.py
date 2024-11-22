from queries import *
from db import cursor, conn, print_table, create_tables, insert_data, print_all_tables


def main():
    while True:
        print("Оберіть запит:")
        print("1. Відобразити всі критичні помилки.")
        print("2. Порахувати кількість помилок кожного рівня.")
        print(
            "3. Порахувати вартість роботи програміста при виправленні кожної помилки."
        )
        print("4. Відобразити всі помилки із заданого джерела.")
        print("5. Порахувати кількість помилок від користувачів та тестувальників.")
        print(
            "6. Порахувати кількість критичних, важливих, незначних помилок кожного програміста."
        )
        print("0. Вийти.")

        choice = input("Ваш вибір: ")
        if choice == "1":
            print_table(*query_critical_errors())
        elif choice == "2":
            print_table(*query_error_levels())
        elif choice == "3":
            print_table(*query_fix_costs())
        elif choice == "4":
            source = input("Введіть джерело (Користувач/Тестувальник): ")
            print_table(*query_errors_by_source(source))
        elif choice == "5":
            print_table(*query_errors_by_users_and_testers())
        elif choice == "6":
            print_table(*query_programmer_error_levels())
        elif choice == "0":
            break
        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    create_tables()
    insert_data()
    print_all_tables()
    main()
    cursor.close()
    conn.close()
