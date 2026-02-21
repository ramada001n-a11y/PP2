# Использование lambda с функцией map для преобразования каждого элемента
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(lambda x: x ** 2, numbers))

print("Исходный список:", numbers)
print("Квадраты чисел:", squared_numbers)