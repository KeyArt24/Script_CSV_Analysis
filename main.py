import argparse, csv, os
from tabulate import tabulate


class ARGS_PARSING():
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog = 'Скрипт для анализа данныых и создания отчёта в CSV формате', usage='%(prog)s [options]', description = self.script_description())
        self.parser.add_argument('-f', '--files', nargs = '+', required = True, help = self.arg_files_help())
        self.parser.add_argument('-r', '--report', default = 'report', help = self.arg_report_help())
        self.parser.add_argument('-pod', '--path_output_dir', default = os.getcwd(), help = self.arg_output_dir())
        self.arguments = self.parser.parse_args()
    
    def arg_files_help(self):
        return 'Обязательный аргумент для запуска скрипта'

    def arg_report_help(self):
        return 'Опция для введение имени отчёта. По умолчанию отчёту присваивается имя report'
    
    def arg_output_dir(self):
        return f'Опция для выбора директории, куда будет сохранятся отчёт. По умолчанию {os.getcwd()}'
    
    def script_description(self):
        return '''Скрипт создан для анализа данных в формате CSV, и создания отчёта 
        по брэндам телефонов c их средним рейтингом, полученный путем сбора данных полученных из всех введённых файлов в анализ.
        Скрипт позволяе танализировать один или несколько файлов, путём добавления через опцию --files.
        Например, для запуска необходимо ввести командную строку python main.py --files ..\\data1.csv ..\\data2.csv'''

class TestPy():
    def test_check_path_file(self):
        assert check_path_file([os.getcwd(), '\\products.csv']) == [os.getcwd()]
    
    def test_avarage_num(self):
        assert avarage_num([2.5, 3, 4.5]) == 3.33
    
    def test_avarage_rating(self):
        list_data = [{'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'}, {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'}, {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'}, {'name': 'iphone 14', 'brand': 'apple', 'price': '799', 'rating': '4.7'}, {'name': 'galaxy a54', 'brand': 'samsung', 'price': '349', 'rating': '4.2'}, {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'}, {'name': 'iphone se', 'brand': 'apple', 'price': '429', 'rating': '4.1'}, {'name': 'galaxy z flip 5', 'brand': 'samsung', 'price': '999', 'rating': '4.6'}, {'name': 'redmi 10c', 'brand': 'xiaomi', 'price': '149', 'rating': '4.1'}, {'name': 'iphone 13 mini', 'brand': 'apple', 'price': '599', 'rating': '4.5'}]
        assert avarage_rating(list_data) == [{'brand': 'apple', 'rating': 4.55}, {'brand': 'samsung', 'rating': 4.53}, {'brand': 'xiaomi', 'rating': 4.37}]

def check_path_file(files: list):
    exsits_files = []
    not_exists_files = []
    for file in files:
        if os.path.exists(file):
            exsits_files.append(file)
        else:
            not_exists_files.append(file)
    if len(not_exists_files) > 0:
        print(f'\nВНИМАНИЕ!!! Некоторые переданные файлы не существуют или не правильно указаны пути до файлов. Проверьте правильность пути.\nЭти файлы не включены в анализ:')
        for file in not_exists_files:
            print(file)
    if len(exsits_files) > 0:
        return exsits_files
    else:
        print('\nДЛЯ АНАЛИЗА НЕТ СООТВЕТСТВУЮЩИХ ФАЙЛОВ')
        exit()

def check_type_file(files: list) -> list:
    csv_files = [] 
    not_csv_files = []
    for file in files:
        try:
            with open(file, 'r', encoding = 'utf-8') as cheking_file:
                csv.Sniffer().sniff(cheking_file.read(1024))
                csv_files.append(file)
        except csv.Error:
            not_csv_files.append(file)
    if len(not_csv_files) > 0:
        print(f'\nВНИМАНИЕ!!! Некоторые переданные файлы не соответствуют формату .csv. Проверьте тип файлов.\nЭти файлы не включены в анализ:')
        for file in not_csv_files:
            print(file) 
    if len(csv_files) > 0:
        return csv_files
    else:
        print('\nДЛЯ АНАЛИЗА НЕТ СООТВЕТСТВУЮЩИХ ФАЙЛОВ')
        exit()       
    
    return csv_files

def read_data(path_to_file: list) -> list:
    list_data = [] 
    for path in path_to_file:
        with open(path, 'r', encoding = 'utf-8') as file:
            data = csv.DictReader(file)
            for row in data:
                list_data.append(row)
    return list_data

def avarage_num(nums: list):
    return round(sum(nums)/len(nums), 2)

def avarage_rating(data: list, flag_1 = 'brand', flag_2 = 'rating') -> list:
    dict_result = {}
    for row in data:
        dict_result.setdefault(row[flag_1], [])
        dict_result[row[flag_1]].append(float(row[flag_2]))
    result = [{flag_1: key, flag_2: avarage_num(value)} for key, value in dict_result.items()]
    result.sort(key = lambda x: x[flag_2], reverse= True)
    return result

def save_data(data: list, name_file: str, directory: str):
    path_output_file = f'{directory}\\{name_file}.csv'
    with open(path_output_file, 'w', newline= '') as file:
        csv_writer = csv.DictWriter(file, fieldnames = data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(data) 

    print(f'\nДанные записаны в {path_output_file}\n')

def run():
    parser = ARGS_PARSING()
    path_files = check_path_file(parser.arguments.files)
    type_files = check_type_file(path_files)
    checked_files = type_files
    data_files = read_data(checked_files)
    analys_rating_brand = avarage_rating(data_files)
    save_data(analys_rating_brand, parser.arguments.report, parser.arguments.path_output_dir)
    print(tabulate(analys_rating_brand, headers = "keys", showindex=range(1, len(analys_rating_brand) + 1), tablefmt="grid"))
    
if __name__ == "__main__":
    run()