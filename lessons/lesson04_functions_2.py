# --- Функция 1: возвращает результат ---
def multiply(a, b):
    return a * b

# --- Функция 2: просто выводит ---
def show_welcome():
    print("Добро пожаловать в программу!")

# --- Функция 3: логическая (возвращает True/False) ---
def is_password_strong(password):
    return len(password) >= 8


# Тестируем функции
show_welcome()

result = multiply(3, 5)
print(f"Результат умножения: {result}")

password = "qwerty123"
if is_password_strong(password):
    print(f"Пароль '{password}' — надёжный")
else:
    print(f"Пароль '{password}' — слабый")

