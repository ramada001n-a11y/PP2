# Разница между переменными класса и переменными экземпляра
class Dog:
    species = "Canis familiaris" # Переменная класса (общая для всех)

    def __init__(self, name):
        self.name = name # Переменная экземпляра (уникальная)

dog1 = Dog("Рекс")
dog2 = Dog("Белка")

print(f"{dog1.name} относится к виду {dog1.species}")
print(f"{dog2.name} относится к виду {dog2.species}")