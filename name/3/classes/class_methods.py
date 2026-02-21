# Добавление методов в класс
class Dog:
    def __init__(self, name):
        self.name = name
        
    def bark(self):
        print(f"{self.name} громко лает: Гав-гав!")

my_dog = Dog("Шарик")
my_dog.bark()