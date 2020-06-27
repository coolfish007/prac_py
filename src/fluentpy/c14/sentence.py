import re
import reprlib

RE_WORD = re.compile("\w+")


class Sentence2:
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return f"Sentence {reprlib.repr(self.text)}"

    def __iter__(self):
        return Sentence2Iterator(self.words)


class Sentence1:
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        """ __getitem__()被Python标识为可迭代对象:
        1. 检查是否实现了__iter__()
        2. 若没有,检查__getitem__(),并创建迭代器,从索引0开始获取元素
        3. 如果失败, Python 抛出 TypeError 异常:'... object is not iterable'
        """
        return self.words[index]

    def __repr__(self):
        return f"Sentence {reprlib.repr(self.text)}"


class Sentence2Iterator:
    def __init__(self, words):
        super().__init__()
        self.worlds = words
        self.index = 0

    def __next__(self):
        try:
            word = self.worlds[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self


class Sentence3(Sentence2):
    def __iter__(self):
        for word in self.words:
            print("in Sentence 3.")
            yield word


class Sentence4(Sentence2):
    def __init__(self, text):
        self.text = text + " end with sentence 4."

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
