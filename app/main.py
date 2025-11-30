import csv
import argparse
from collections import defaultdict
from typing import List, Dict, Tuple
from tabulate import tabulate
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Dataclass для представления строки из CSV-файла
@dataclass
class Developer:
	name: str
	position: str
	completed_tasks: int
	performance: float
	skills: str
	team: str
	experience_years: int

# Абстрактный класс для отчётов
class BaseReport(ABC):
	@abstractmethod
	def generate(self, data: List[Developer]) -> List[Tuple[str, float]]:
			pass

# Конкретный класс для отчёта о средней эффективности
class PerformanceReport(BaseReport):
	def generate(self, data: List[Developer]) -> List[Tuple[str, float]]:
			averages = defaultdict(lambda: {'total': 0, 'count': 0})
			for entry in data:
					pos = entry.position
					perf = entry.performance
					averages[pos]['total'] += perf
					averages[pos]['count'] += 1

			report = [(pos, round(stats['total'] / stats['count'], 2)) for pos, stats in averages.items()]
			report.sort(key=lambda x: x[1], reverse=True)
			return report

# Чтение данных из CSV-файла
def read_csv(file_path: str) -> List[Developer]:
	"""Читает данные из CSV-файла и возвращает список объектов Developer."""
	with open(file_path, newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			return [Developer(
					name=row['name'],
					position=row['position'],
					completed_tasks=int(row['completed_tasks']),
					performance=float(row['performance']),  # Преобразуем строку в число
					skills=row['skills'],
					team=row['team'],
					experience_years=int(row['experience_years'])
			) for row in reader]

# Вывод отчёта в консоль или сохранение в файл
def generate_report(report: List[Tuple[str, float]], output_file: str = None):
	"""Выводит отчёт в консоль или сохраняет в файл.
		Если указан output_file, отчёт сохраняется в файл, иначе выводится в консоль.
	"""
	if output_file:
			with open(output_file, 'w', encoding='utf-8') as out:
					out.write("Position, Average Performance\n")
					for pos, avg in report:
							out.write(f"{pos}, {avg}\n")
	else:
# Используем tabulate для вывода таблицы в консоль
			print(tabulate(report, headers=["Position", "Average Performance"], tablefmt="grid"))

# Основной блок выполнения
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Performance Report Generator")
	parser.add_argument("--files", nargs="+", required=True, help="Input CSV files.")
	# Удаляем обязательность параметра --report
	parser.add_argument("--report", choices=['performance'], help="Name of the report")
	args = parser.parse_args()

# Чтение данных из всех файлов
	data = []
	for file in args.files:
			try:
					data.extend(read_csv(file))
			except Exception as err:
					print(f"Ошибка при чтении файла '{file}': {err}. Не найден.")
		
# Создание объекта отчёта
	report_generator = PerformanceReport()
	processed_data = report_generator.generate(data)
	generate_report(processed_data)