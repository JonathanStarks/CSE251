name1 = "bob\tsmith"
name2 = r"bob\tsmith"

print(name1)
print(name2)

class Person:
    def __init__(self, name):
        self.name = name
        
    def display(self):
        print(self.name)

fred = Person("Fred")
fred.display()