class Bird:
    feather = True

    def chirp(self):
        print(self)
        print("bird some sound")

    @classmethod
    def funcname(*args):
        print(args)
        print("bird classmethod")


class Chicken(Bird):
    fly = False

    def __init__(self, age) -> None:
        self.age = age

    def chirp(self):
        print("jijiji")

    def display_super(self):
        pass
