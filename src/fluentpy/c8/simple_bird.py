class Bird:
    feather = True

    def chirp():
        print("bird some sound")


class Chicken(Bird):
    fly = False

    def __init__(self, age) -> None:
        self.age = age

    def chirp():
        print("jijiji")
