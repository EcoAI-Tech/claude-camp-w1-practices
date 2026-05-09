def life_stage(age):
    if age < 13:
        return "child"
    if age < 20:
        return "teenager"
    if age < 60:
        return "adult"
    return "senior"


def main():
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    try:
        age = int(input("Enter your age: "))
    except ValueError:
        print("Age must be an integer.")
        return
    if age < 0 or age > 150:
        print("Age out of range.")
        return
    stage = life_stage(age)
    print(f"Hello, {name}! You are {age} years old, a {stage}.")
    print(f"Nice to meet you, {name}. Have a wonderful day!")


if __name__ == "__main__":
    main()
