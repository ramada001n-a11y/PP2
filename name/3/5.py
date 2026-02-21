class Shape:
    def area():
       return 0
    
class Square(Shape):
    def __init__(self,length):
        self.length = length

    def area(self):
        return self.length * self.length

n = int(input())

sqr = Square(n)  
print(sqr.area())