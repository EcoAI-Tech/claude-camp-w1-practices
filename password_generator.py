import secrets
import string


def generate(length):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main():
    try:
        length = int(input("Enter password length: "))
    except ValueError:
        print("Length must be an integer.")
        return
    if length < 4:
        print("Length must be at least 4.")
        return
    if length > 128:
        print("Length must be at most 128.")
        return
    password = generate(length)
    print(f"Generated password: {password}")


if __name__ == "__main__":
    main()
