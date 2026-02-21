class StringHand:
    def getString(self, text):
        self.text = text 

    def printString(self):
        print(self.text.upper())  


b = input() 

a = StringHand()              
a.getString(b)                
a.printString()               