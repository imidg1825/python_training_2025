print("=== Проверка доступа ===")

age = int(input("Введите ваш возраст: "))
has_passport = input("Есть ли у вас паспорт? (да/нет): ")
is_with_parents = input("Вы с родителями? (да/нет): ")

# Переводим ответы в True/False
has_passport = has_passport == "да"
is_with_parents = is_with_parents == "да"

print()  # пустая строка для красоты
print(f"[DEBUG] Ввод пользователя: возраст={age}, паспорт={has_passport}, с_родителями={is_with_parents}")

# Логика доступа
if age >= 18 and has_passport:
    print(f"Доступ разрешён: взрослый с паспортом (возраст {age})")

elif age < 18 and is_with_parents:
    print(f"Доступ разрешён: несовершеннолетний, но с родителями (возраст {age})")

elif age >= 18 and not has_passport:
    print(f"Доступ запрещён: вы совершеннолетний, но без паспорта (возраст {age})")

else:
    print(f"Доступ запрещён: возраст {age} слишком маленький")

print("Готово!")
