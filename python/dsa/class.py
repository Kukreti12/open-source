class Employee:
    def __init__(self,name) -> None:
        self.name=name
    def run(self):
        print(self.name)
    @staticmethod
    def sleepwell():
        print("kindly sleep well")


test2=Employee("mike")
test2.run()

