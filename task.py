from typing import List, Dict, Union, Callable
import csv
import argparse
from tabulate import tabulate
from statistics import median

def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Читает CSV-файл в список словарей."""
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            if not data:
                print(f"Файл {file_path} пуст или содержит только заголовки")
                return []
            return data
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        return []
    except csv.Error as e:
        print(f"Ошибка парсинга CSV: {e}")
        return []

def filter_data(data: List[Dict[str, str]], where: str) -> List[Dict[str, str]]:
    """Фильтрует данные по условию column=opvalue."""
    if not where:
        return data
    try:
        if '=' in where:
            column, value = where.split('=', 1)
            op = '='
        elif '>' in where:
            column, value = where.split('>', 1)
            op = '>'
        elif '<' in where:
            column, value = where.split('<', 1)
            op = '<'
        else:
            raise ValueError("Некорректный оператор в --where")

        if not any(column in row for row in data):
            raise ValueError(f"Столбец {column} не найден в данных")

        is_numeric = all(row[column].replace('.', '', 1).isdigit() for row in data if row[column])

        def apply_filter(row: Dict[str, str]) -> bool:
            row_value = row[column]
            if is_numeric:
                row_value = float(row_value)
                value_float = float(value)
                if op == '=':
                    return row_value == value_float
                elif op == '>':
                    return row_value > value_float
                elif op == '<':
                    return row_value < value_float
            else:
                if op == '=':
                    return row_value.lower() == value.lower()  # Регистронезависимое сравнение
                raise ValueError("Только = поддерживается для текстовых колонок")
            return False

        return [row for row in data if apply_filter(row)]
    except (ValueError, KeyError) as e:
        print(f"Ошибка в фильтрации: {e}")
        return data

def aggregate_data(data: List[Dict[str, str]], aggregate: str) -> Union[float, None]:
    """Выполняет агрегацию по column=agg_type (avg, min, max, median)."""
    if not aggregate or not data:
        return None
    try:
        column, agg_type = aggregate.split('=', 1)
        agg_functions: Dict[str, Callable[[List[float]], float]] = {
            'avg': lambda x: sum(x) / len(x),
            'min': min,
            'max': max,
            'median': median
        }
        if agg_type not in agg_functions:
            raise ValueError("Агрегация должна быть avg, min, max или median")
        values = [float(row[column]) for row in data]
        return agg_functions[agg_type](values)
    except (ValueError, KeyError) as e:
        print(f"Ошибка в агрегации: {e}")
        return None

def sort_data(data: List[Dict[str, str]], sort: str) -> List[Dict[str, str]]:
    """Сортирует данные по column=order (asc, desc) с поддержкой текстовых колонок."""
    if not sort:
        return data
    try:
        column, order = sort.split('=', 1)
        if order not in ['asc', 'desc']:
            raise ValueError("Порядок сортировки: asc или desc")
        if not any(column in row for row in data):
            raise ValueError(f"Столбец {column} не найден в данных")

        def get_key(row: Dict[str, str]) -> Union[float, str]:
            value = row[column]
            return float(value) if all(r[column].replace('.', '', 1).isdigit() for r in data if r[column]) else value.lower()

        return sorted(data, key=get_key, reverse=(order == 'desc'))
    except (ValueError, KeyError) as e:
        print(f"Ошибка в сортировке: {e}")
        return data

def main():
    parser = argparse.ArgumentParser(description="Обработка CSV-файла")
    parser.add_argument('file', help='Путь к CSV-файлу')
    parser.add_argument('--where', help='Фильтрация: column=opvalue (например, name=Samsung)')
    parser.add_argument('--aggregate', help='Агрегация: column=agg_type (например, price=median)')
    parser.add_argument('--order-by', help='Сортировка: column=order (например, name=desc)')
    args = parser.parse_args()

    # Чтение файла
    data = read_csv(args.file)
    if data is None or not data:
        return

    # Сортировка
    data = sort_data(data, args.order_by)

    # Фильтрация
    data = filter_data(data, args.where)

    # Вывод результатов
    if args.aggregate:
        result = aggregate_data(data, args.aggregate)
        if result is not None:
            table_data = [['Aggregation', 'Value'], [args.aggregate, result]]
            print("Данные для таблицы:", table_data)
            print(tabulate(table_data, tablefmt='grid'))
        else:
            print("Нет данных для агрегации (возможно, фильтр исключил все строки)")
    else:
        if data:
            print(tabulate(data, headers='keys', tablefmt='grid'))
        else:
            print("Нет данных для вывода")

if __name__ == '__main__':
    main()