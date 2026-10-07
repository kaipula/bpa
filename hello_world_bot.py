from datetime import datetime

print("Hello World!")
name = input("Enter your name: ")
print(f"Good Morning, {name}! I am HelloBot.")

# Basic variables
age = 21
cgpa = 8.75
is_student = True
today = datetime.now()

print("\n=== Basic Variables ===")
for label, value in [("name", name), ("age", age), ("cgpa", cgpa),
                     ("is_student", is_student), ("today", today)]:
    print(f"{label:<13}= {str(value):<29}type: {type(value).__name__}")

# Type conversion
print("\n=== Type Conversion ===")
print(f"str(age)        -> {str(age)!r} ({type(str(age)).__name__})")
print(f"int('95')       -> {int('95')} ({type(int('95')).__name__})")
print(f"float('88.5')   -> {float('88.5')} ({type(float('88.5')).__name__})")

# Collections
subjects = ["HCI", "BPA", "Design Patterns", "Cloud Computing"]
student = {"name": name, "age": age, "cgpa": cgpa}
print("\n=== Collections ===")
print(f"List       : {subjects}")
print(f"Dictionary : {student}")
print(f"Count      : {len(subjects)}")

# String operations
text = "  business process automation  "
print("\n=== String Operations ===")
print(f"Trim      : {text.strip()}")
print(f"Upper     : {text.strip().upper()}")
print(f"Title     : {text.strip().title()}")
print(f"Replace   : {text.strip().replace('automation', 'bot')}")
print(f"Split     : {text.strip().split()}")
print(f"Contains  : {'process' in text}")

# Arithmetic
a, b = 25, 4
print("\n=== Arithmetic ===")
print(f"{a}+{b}={a + b}, {a}-{b}={a - b}, {a}*{b}={a * b}, {a}/{b}={a / b}, {a}%{b}={a % b}")

print(f"\nBye {name}, HelloBot signing off!")
