class HauntedBus:
    """ 可变类型做为默认参数,造成的bug """

    def __init__(self, passengers=[]) -> None:
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)
