num1 = int(input("Enter a number: "))
num2 = int(input("Enter a second number: "))
operator = input("Enter an operator (either + or -): ")

if operator == "+":
    print(num1 + num2)
elif operator == "-":
    print(num1 - num2)
else:
    print("Unknown Operator")