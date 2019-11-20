

class Singleton:
    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise Exception("this class is singleton class")
        Singleton._instance = self

    @staticmethod
    def getintance():
        if Singleton._instance is None:
            Singleton()
        return Singleton._instance


z=Singleton.getintance()
print(z)