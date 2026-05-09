def classify(bmi):
    if bmi < 18.5:
        return "Underweight", "Consider a balanced diet to gain weight."
    if bmi < 25:
        return "Normal", "Great! Keep up your healthy lifestyle."
    if bmi < 30:
        return "Overweight", "Try regular exercise and watch your diet."
    return "Obese", "Please consult a doctor for health guidance."


def main():
    try:
        height_cm = float(input("Enter height (cm): "))
        weight_kg = float(input("Enter weight (kg): "))
    except ValueError:
        print("Invalid number.")
        return
    if height_cm <= 0 or weight_kg <= 0:
        print("Height and weight must be positive.")
        return
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    category, advice = classify(bmi)
    print(f"BMI: {bmi:.2f}")
    print(f"Category: {category}")
    print(f"Advice: {advice}")


if __name__ == "__main__":
    main()
