def make_sum_average():
    series = []

    def average(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return average


def make_average():
    count = 0
    total = 0

    def average(new_value):
        # 不可变元素声明为自由变量
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return average
