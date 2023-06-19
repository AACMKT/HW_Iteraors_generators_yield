""" Доработать класс FlatIterator в коде ниже.
    Должен получиться итератор, который принимает список списков и возвращает их плоское представление,
    т. е. последовательность, состоящую из вложенных элементов.
    Функция test в коде ниже также должна отработать без ошибок."""

from itertools import chain
import types


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.counter = 0
        self.y = 0
        return self

    def __next__(self):
        self.n = len(self.list_of_list)

        if self.counter < self.n:
            self.m = len(self.list_of_list[self.counter])
            item = self.list_of_list[self.counter][self.y]
            if self.y < self.m - 1:
                self.y += 1
            else:
                self.y = 0
                self.counter += 1
        else:
            raise StopIteration

        return item


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


# if __name__ == '__main__':
#     test_1()

""" Доработать функцию flat_generator.
    Должен получиться генератор, который принимает список списков и возвращает их плоское представление.
    Функция test в коде ниже также должна отработать без ошибок."""


def flat_generator(list_of_lists):
    # for j in list_of_lists:
    #     for i in j:
    #         yield i
    counter = 0
    while counter < len(list_of_lists):
        for i in list_of_lists[counter]:
            yield i
        counter += 1


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


# if __name__ == '__main__':
#     test_2()

""" Необязательное задание.
    Написать итератор, аналогичный итератору из задания 1, но обрабатывающий списки с любым уровнем вложенности.
    Шаблон и тест в коде ниже:"""

""" Первый способ """

# class FlatIteratorAdv:
#
#     def __init__(self, list_of_list):
#         self.list_of_list = list_of_list
#
#     def __iter__(self):
#         self.counter = 0
#         self.val = (((((str(self.list_of_list).replace("[", "")).replace("]", ""))
#                        .replace(",", "")).replace("'", "")).split(' '))
#         for i in self.val:
#             if "" == i:
#                 self.val.remove(i)
#         return self
#
#     def __next__(self):
#         self.n = len(self.val)
#         if self.counter < self.n:
#             item = self.val[self.counter]
#             self.counter += 1
#             if item in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
#                 item = int(item)
#             elif item in ['True', 'False', 'None']:
#                 item = eval(item)
#         else:
#             raise StopIteration
#
#         return item

""" Второй способ """


class FlatIteratorAdv:

    def __init__(self, list_of_list):
        self.lst = list(chain.from_iterable(list_of_list))
        self.lst = list(chain.from_iterable(list_of_list))
        self.new_lst = []
        self.counter = 0
        self.a = 0

    def __iter__(self):
        while self.a <= len(self.lst):
            for x in range(len(self.lst)):
                if isinstance(self.lst[x], list):
                    self.lst[x] = list(chain.from_iterable(self.lst[x]))
                    self.a -= 1

                else:
                    self.a += 1
                if type(self.lst[x]) is list:
                    self.new_lst += self.lst[x]
                else:
                    self.new_lst.append(self.lst[x])
                # print(i)
            self.lst = self.new_lst
            self.new_lst = []
        return self

    def __next__(self):
        if self.counter < len(self.lst):
            item = self.lst[self.counter]
            self.counter += 1
            return item
        else:
            raise StopIteration


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIteratorAdv(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIteratorAdv(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


# if __name__ == '__main__':
#     test_3()

""" Необязательное задание. Написать генератор, аналогичный генератору из задания 2,
    но обрабатывающий списки с любым уровнем вложенности.
    Шаблон и тест в коде ниже:"""


def flat_generator_adv(list_of_list):
    new_list = []
    counter = 0
    while counter <= len(list_of_list):
        for i in list_of_list:
            if isinstance(i, list):
                new_list += i
                counter -= 1
            else:
                new_list.append(i)

        counter += 1
        list_of_list = new_list
        new_list = []
    for i in list_of_list:
        yield i


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_adv(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_adv(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator_adv(list_of_lists_2), types.GeneratorType)

# if __name__ == '__main__':
#     test_4()
