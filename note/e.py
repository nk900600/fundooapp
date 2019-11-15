#

class Salary:

    def __init__(self,pay,bonus):
        self.name=pay
        self.place=bonus

    def annual(self):
        return self.name

class Empoyee:

    def __init__(self,name,place):
        self.name=name
        self.place=place

    def annual(self):
        return self.name
    def __eq__(self, other):
        if isinstance(other,Empoyee):

            return self.name==other.name and self.place== other.place
        return "yo"

#

# s= Salary(5000,5000)
c= Empoyee("nik","mumbai")
z=Salary("nik","fde")
print(c.__eq__(z))


class Meter:
    '''Descriptor for a meter.'''
    name="fvgf"

    def __init__(self, value=0.0):
        self.value = float(value)
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        self.value = float(value)




class Distance:
    '''Class to represent distance holding two descriptors for feet and
    meters.'''
    meter = Meter()


d= Distance
m=Meter(54)
print(m.__get__(m,d))

#
# class Word(str):
#     '''Class for words, defining comparison based on word length.'''
#
#     def __new__(cls, word):
#         # Note that we have to use __new__. This is because str is an immutable
#         # type, so we have to initialize it early (at creation)
#         if ' ' in word:
#             print("Value contains spaces. Truncating to first space.")
#             word = word[:word.index(' ')] # Word is now all chars before first space
#         return str.__new__(cls, word)
#
#     def __gt__(self, other):
#         return len(self) > len(other)
#     def __lt__(self, other):
#         return len(self) < len(other)
#     def __ge__(self, other):
#         return len(self) >= len(other)
#     def __le__(self, other):
#         return len(self) <= len(other)
#
#
# z= Word("dvdf ")
# print(z)