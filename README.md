# README.md
## Примеры запуска
- Все данные: `python task.py products.csv`
- Фильтр: `python task.py products.csv --where "brand=SAMSUNG"`
- Агрегация: `python task.py products.csv --aggregate "price=median"`
- Сортировка: `python task.py products.csv --order-by "price=desc"`
- Комбинация: `python task.py products.csv --where "rating>4.0" --order-by "name=asc" --aggregate "price=max"`
- Ошибка: `python task.py products.csv --where "color=Red"`