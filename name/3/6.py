class Shape:
    def area():
       return 0
    
# class Square(Shape):
#     def __init__(self,length):
#         self.length = length

#     def area(self):
#         return self.length * self.length
class Rectangle(Shape):
    def __init__(self,length,width):
        self.length = length
        self.width = width
        
    def area(self):
        return self.length * self.width
    

w = list(map(int,input().split()))
sqr = Rectangle(w[0],w[1])



print(sqr.area())