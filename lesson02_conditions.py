# Урок 2: Условия (if / elif / else)

print("=== Проверка возраста ===")

age = int(input("Сколько вам лет? "))

if age < 7:
    print(f"Вам {age} лет — вы дошкольник")
elif age < 18:
    print(f"Вам {age} лет — вы школьник")
elif age < 25:
    print(f"Вам {age} лет — вы студент")
else:
    print(f"Вам {age} лет — вы взрослый человек")

print("Готово!")
