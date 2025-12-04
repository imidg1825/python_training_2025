import random  # подключаем модуль для случайных чисел

print("Привет! Я загадал число от 1 до 20.")
print("Попробуй угадать его за 5 попыток!")

secret = random.randint(1, 20)  # тут компьютер загадывает число
attempt = 1  # номер попытки

while attempt <= 5:
    print()
    print("Попытка номер", attempt)
    guess_text = input("Введи число от 1 до 20: ")

    # превращаем текст из input в число
    guess = int(guess_text)

    if guess == secret:
        print("Ура! Ты угадал число!", secret)
        print("Тебе понадобилось попыток:", attempt)
        break  # выходим из цикла, игра закончена
    elif guess < secret:
        print("Моё число БОЛЬШЕ.")
    else:
        print("Моё число МЕНЬШЕ.")

    attempt = attempt + 1  # не забываем увеличивать номер попытки

# этот блок сработает, если НЕ было break (то есть не угадали за 5 раз)
if attempt > 5 and guess != secret:
    print()
    print("Попытки закончились :(")
    print("Я загадал число:", secret)

print()
print("Игра окончена. Спасибо за игру!")
