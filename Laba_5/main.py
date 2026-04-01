def lcg(seed, a=1664525, c=1013904223, m=2**32):
    """Линейный конгруэнтный генератор"""
    x = seed
    while True:
        x = (a * x + c) % m
        yield x


def otp_generator():
    try:
        passport = input("Введите номер паспорта: ")
        birthdate = input("Введите дату рождения (цифрами): ")
        phone = input("Введите номер телефона: ")

        user_data = passport + birthdate + phone
        digits = [ch for ch in user_data if ch.isdigit()]

        if len(digits) == 0:
            print("Не введено ни одной цифры.")
            return

        while len(digits) < 20:
            digits.extend(digits)

        digits = digits[:20]

        n = 12
        otp = ""

        seed = sum(int(d) for d in digits)
        generator = lcg(seed)

        for _ in range(n):
            index = next(generator) % len(digits)
            otp += digits[index]

        print("Массив цифр пользователя:", digits)
        print("Одноразовый пароль:", otp)

    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    otp_generator()