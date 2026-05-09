def c_to_f(c):
    return c * 9 / 5 + 32


def f_to_c(f):
    return (f - 32) * 5 / 9


def main():
    print("Temperature Converter")
    print("1. Celsius -> Fahrenheit")
    print("2. Fahrenheit -> Celsius")
    choice = input("Choose (1/2): ").strip()
    try:
        value = float(input("Enter temperature: "))
    except ValueError:
        print("Invalid number.")
        return
    if choice == "1":
        print(f"{value} C = {c_to_f(value):.2f} F")
    elif choice == "2":
        print(f"{value} F = {f_to_c(value):.2f} C")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
