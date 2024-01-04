import pytest
from cjen.nene.collection_utils import list_eql

from pyodm.factory.xpath.direction import Direction
from pyodm.factory.xpath.xpath_node import XpathNode
from pyodm.factory.xpath.xpath_tree import XpathTree


@pytest.fixture
def test_data1():
    return {
        "A": ["A1", "A2", "A3"],
        "B": ["B1", "B2", "B3"],
        "A1": ["C1", "B", "C2"]
    }


def test_case1(test_data1):
    xtree = XpathTree()
    for key, children in test_data1.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert xtree.count() == 10
    for node in xtree.children_by_name("A"):
        assert node.name in ["A1", "A2", "A3"]
    for node in xtree.children_by_name("A1"):
        assert node.name in ["C1", "B", "C2"]
    for node in xtree.children_by_name("B"):
        assert node.name in ["B1", "B2", "B3"]


@pytest.fixture
def test_data2():
    return {
        "A": ["A1", "A2", "A3"],
        "B": ["B1", "B2", "B3"],
        "C": ["A", "B"]
    }


def test_case2(test_data2):
    xtree = XpathTree()
    for key, children in test_data2.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert xtree.count() == 9
    for node in xtree.children_by_name("A"):
        assert node.name in ["A1", "A2", "A3"]
    for node in xtree.children_by_name("B"):
        assert node.name in ["B1", "B2", "B3"]
    for node in xtree.children_by_name("C"):
        assert node.name in ["A", "B"]


@pytest.fixture
def test_data3():
    return {
        "A": ["A1", "A2", "A3"],
        "B": ["B", "B2", "B3"],
        "C": ["A", "B"]
    }


def test_case3(test_data3):
    xtree = XpathTree()
    for key, children in test_data3.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert xtree.count() == 8
    for node in xtree.children_by_name("A"):
        assert node.name in ["A1", "A2", "A3"]
    for node in xtree.children_by_name("B"):
        assert node.name in ["B", "B2", "B3"]
    for node in xtree.children_by_name("C"):
        assert node.name in ["A", "B"]
    print(xtree._all_path_index())


@pytest.fixture
def test_data4():
    return {
        "A": ["B", "A2"],
        "B": ["B1", "B2", "B3"],
        "B1": ["C1", "C2", "C3", "C4"],
    }


def test_case4(test_data4):
    xtree = XpathTree()
    for key, children in test_data4.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert list_eql(['A/B/B1/C1', 'A/B/B1/C2', 'A/B/B1/C3', 'A/B/B1/C4', 'A/B/B2', 'A/B/B3', 'A/A2'], xtree.xpath())
    # assert ['A/B/B1/C1', 'A/B/B1/C2', 'A/B/B1/C3', 'A/B/B1/C4', 'A/B/B2', 'A/B/B3', 'A/A2'] == xtree.xpath()


@pytest.fixture
def test_data5():
    return {
        "A": ["B", "A2"],
        "B": ["B", "B2", "B3"],
        "B1": ["C1", "C2", "C3", "C4"],
    }


def test_case5(test_data5):
    """
    父节点中的子节点包含父节点 "B": ["B", "B2", "B3"]
    """
    xtree = XpathTree()
    for key, children in test_data5.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert list_eql(['A/B/B2', 'A/B/B3', 'A/A2', 'B1/C1', 'B1/C2', 'B1/C3', 'B1/C4'], xtree.xpath())


@pytest.fixture
def test_data6():
    return {
        "A": ["B", "A2"],
        "B": ["B", "B2", "B3"],
        "B1": ["B", "C2"],
    }


def test_case6(test_data6):
    """
    子节点包含其它父节点 "B1": ["B", "C2"]
    """
    xtree = XpathTree()
    for key, children in test_data6.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert list_eql(['A/B/B2', 'A/B/B3', 'A/A2', 'B1/B/B2', 'B1/B/B3', 'B1/C2'], xtree.xpath())



@pytest.fixture
def test_data7():
    return {
        "A": ["B", "B"],
        "B": ["B", "B2", "B3"],
        "B1": ["B", "C2"],
    }


def test_case7(test_data7):
    """
    去重
    """
    xtree = XpathTree()
    for key, children in test_data7.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert list_eql(['A/B/B2', 'A/B/B3', 'B1/B/B2', 'B1/B/B3', 'B1/C2'], xtree.xpath())


@pytest.fixture
def test_data8():
    return {
        "A": ["B", "B"],
        "B": ["B", "B2", "B3"],
        "B1": ["B", "C2"],
    }


def test_case8(test_data8):
    """
    获取 XPATH 的方式
    """
    xtree = XpathTree()
    for key, children in test_data8.items():
        xtree.add(XpathNode(key), [XpathNode(child) for child in children])
    assert list_eql(['A/B/B2', 'A/B/B3'], xtree.xpath("A"))
    assert list_eql(['A/B/B3', 'B1/B/B3'], xtree.xpath("B3", Direction.TO))
    assert list_eql(['A/B/B2', 'A/B/B3', 'B1/B/B2', 'B1/B/B3'], xtree.xpath("B", Direction.INCLUDE))

    # assert ['A/B/B2', 'A/B/B3'] == xtree.xpath("A")
    # assert ['A/B/B3', 'B1/B/B3'] == xtree.xpath("B3", Direction.TO)
    # assert ['A/B/B2', 'A/B/B3', 'B1/B/B2', 'B1/B/B3'] == xtree.xpath("B", Direction.INCLUDE)
