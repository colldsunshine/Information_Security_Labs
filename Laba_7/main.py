import random

password = "security"

positions = random.sample(range(len(password)), 2)

print("Введите символы пароля:")

user_input = []

for pos in positions:
    value = input(f"Символ на позиции {pos + 1}: ")
    user_input.append(value)

correct = True

for i, pos in enumerate(positions):
    if user_input[i] != password[pos]:
        correct = False

if correct:
    print("Доступ разрешён")
else:
    print("Доступ запрещён")
