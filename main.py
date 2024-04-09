import time

from cryptography.fernet import Fernet


def encrypt_text(text, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text.encode()).decode()


def decrypt_text(encrypted_text, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_text.encode()).decode()


def measure_typing_speed_register(phrase):
    all_time = 0
    middle_time = 0
    for _ in range(4):
        start_time = time.time()
        input_phrase = input("Введите фразу '" + phrase + "': ")
        if input_phrase != phrase:
            print("Ошибка! Фраза введена неверно")
            return -1
        end_time = time.time()
        all_time += end_time - start_time
    middle_time = all_time / 4
    print(middle_time)

    return middle_time


def measure_typing_speed_auth(phrase):
    start_time = time.time()
    input_phrase = input("Введите фразу '" + phrase + "': ")
    if input_phrase != phrase:
        print("Ошибка! Фраза введена неверно")
        return -1
    end_time = time.time()
    return end_time - start_time


def register_user(phrase_file, key):
    login = input("Введите логин > ")
    with open('users.txt', 'r') as f:
        for line in f:
            data = line.split(" ")
            if login == data[0]:
                print("Ошибка! Пользователь уже существует.")
                return -1
    password = input("Введите пароль > ")

    with open(phrase_file, 'r') as f:
        phrase = decrypt_text(f.read(), key)
    time = measure_typing_speed_register(phrase)
    if time == -1:
        return -1

    with open('users.txt', 'a') as f:
        f.write("\n")
        f.write(login + " " + password + " " + str(time) + " " + encrypt_text(phrase, key))


def authenticate_user(phrase_file, key):
    flag = False
    login = input("Введите логин > ")
    password = input("Введите пароль > ")
    with open(phrase_file, 'r') as f:
        phrase = decrypt_text(f.read(), key)
    with open('users.txt', 'r') as f:
        for line in f:
            data = line.split(" ")
            if data[0] == login and data[1] == password:
                flag = True
                auth_time = measure_typing_speed_auth(phrase)
                if auth_time == -1:
                    return -1
                if abs(float(data[2]) - auth_time) > 0.5:
                    print(f"Отказ в доступе. Отклонение выше нормы: {abs(float(data[2]) - auth_time)}")
                else:
                    print("Вход успешно произведен")
        if not flag:
            print("Неверный логин или пароль")


def main():
    phrases_file = 'phrases.txt'
    key = Fernet.generate_key()
    phrase = "LlirSTLcOUBbdFuwarjmMgWYrRkWBB"

    encrypt_phrase = encrypt_text(phrase, key)
    open(phrases_file, 'w').close()

    with open(phrases_file, 'w') as f:
        f.write(encrypt_phrase)
    print("Добро пожаловать! Войдите в систему, чтобы продолжить.")
    while True:
        print("""
1. Регистрация
2. Авторизация
3. Выход
        """)
        choice = int(input(">"))

        if choice == 1:
            register_user(phrases_file, key)
        elif choice == 2:
            authenticate_user(phrases_file, key)
        else:
            break


if __name__ == "__main__":
    main()
