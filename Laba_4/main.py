def keylogger_simulation(filename):
    try:
        login = input("Введите логин: ")
        password = input("Введите пароль: ")

        data = f"Логин: {login} | Пароль: {password}\n"

        with open(filename, "a", encoding="utf-8") as file:
            file.write(data)

        print("Данные успешно записаны в файл.")

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    filename = input("Введите имя файла: ")
    keylogger_simulation(filename)