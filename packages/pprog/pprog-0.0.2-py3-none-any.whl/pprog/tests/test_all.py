from collections import namedtuple
from pprog import attrgetter, itemgetter, identity, ConstantCreator, perm, PermArgsExecutor


def test_attrgetter():
    name = namedtuple("Name", ["first", "last"])
    name.first = "Zhiqing"
    name.last = "Xiao"
    person = namedtuple("Person", ["name", "city"])
    person.name = name
    person.city = "Beijing"

    g = attrgetter("city")
    result = g(person)
    assert result == "Beijing"
    g = attrgetter("city", "hometown", default=None)
    result = g(person)
    assert result == ("Beijing", None)
    g = attrgetter("name.first", "name.middle", "name.last", default="")
    result = g(person)
    assert result == ("Zhiqing", "", "Xiao")


def test_itemgetter():
    person = {"name": {"first": "Zhiqing", "last": "Xiao"}, "city": "Beijing"}

    g = itemgetter("city")
    result = g(person)
    assert result == "Beijing"
    g = itemgetter("city", "hometown", default=None)
    result = g(person)
    assert result == ("Beijing", None)
    g = itemgetter(["name", "first"], ["name", "middle"], ["name", "last"], default="")
    result = g(person)
    assert result == ("Zhiqing", "", "Xiao")


def test_identity():
    result = identity(3, "hello", key="value")
    assert result == 3


def test_ConstantCreator():
    creator = ConstantCreator(4)
    result = creator()
    assert result == 4


def test_perm():
    result = perm(["a", "b", "c", "d", "e", "f", "g"], [1, 2, 4])
    assert result == ["a", "c", "e", "d", "b", "f", "g"]


def test_PermArgsExecutor():
    executor = PermArgsExecutor(range)
    result = executor(4, 2)
    assert result == range(2, 4)
