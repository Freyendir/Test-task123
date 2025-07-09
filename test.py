import pytest
from task import read_csv, filter_data, aggregate_data, sort_data

# Тестовые данные
TEST_DATA = [
    {"name": "Apple", "price": "999.99", "rating": "4.7"},
    {"name": "Samsung", "price": "899.50", "rating": "4.5"},
    {"name": "Nokia", "price": "600", "rating": "3.1"}
]

def test_read_csv():
    with open("test.csv", "w") as f:
        f.write("name,price,rating\nApple,999.99,4.7")
    assert read_csv("test.csv") == [{"name": "Apple", "price": "999.99", "rating": "4.7"}]
    assert read_csv("nonexistent.csv") == []

def test_filter_data():
    assert filter_data(TEST_DATA, "rating>4.0") == [
        {"name": "Apple", "price": "999.99", "rating": "4.7"},
        {"name": "Samsung", "price": "899.50", "rating": "4.5"}
    ]
    assert filter_data(TEST_DATA, "name=Apple") == [{"name": "Apple", "price": "999.99", "rating": "4.7"}]
    assert filter_data(TEST_DATA, "brand=Apple") == TEST_DATA  # Ошибка обработана

def test_aggregate_data():
    assert aggregate_data(TEST_DATA, "price=avg") == pytest.approx(833.16, 0.01)
    assert aggregate_data(TEST_DATA, "price=max") == 999.99
    assert aggregate_data(TEST_DATA, "price=median") == 899.50
    assert aggregate_data([], "price=avg") is None

def test_sort_data():
    result = sort_data(TEST_DATA, "price=asc")
    assert [row["price"] for row in result] == ["600", "899.50", "999.99"]
    result = sort_data(TEST_DATA, "name=desc")
    assert [row["name"] for row in result] == ["Samsung", "Nokia", "Apple"]

if __name__ == "__main__":
    pytest.main(["-v", "--cov=123.py"])