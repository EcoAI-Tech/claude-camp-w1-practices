def calculate(bill, tip_percent):
    tip = bill * tip_percent / 100
    total = bill + tip
    return tip, total


def main():
    try:
        bill = float(input("Enter bill amount: "))
        tip_percent = float(input("Enter tip percentage (e.g. 15): "))
    except ValueError:
        print("Invalid number.")
        return
    if bill < 0 or tip_percent < 0:
        print("Values must be non-negative.")
        return
    tip, total = calculate(bill, tip_percent)
    print(f"Bill:   ${bill:.2f}")
    print(f"Tip:    ${tip:.2f} ({tip_percent:.1f}%)")
    print(f"Total:  ${total:.2f}")


if __name__ == "__main__":
    main()
