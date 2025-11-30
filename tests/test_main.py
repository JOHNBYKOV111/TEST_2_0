import csv
import pytest
from app.main import read_csv, generate_report, Developer, PerformanceReport
from tabulate import tabulate

# Фикстура для предоставления тестовых данных
@pytest.fixture
def sample_data():
	return [
			Developer(name='John Doe', position='Backend Developer', completed_tasks=45, performance=4.8, skills='Python, Django', team='API Team', experience_years=5),
			Developer(name='Jane Smith', position='Frontend Developer', completed_tasks=38, performance=4.7, skills='React, TypeScript', team='Web Team', experience_years=4),
			Developer(name='Alice Johnson', position='Backend Developer', completed_tasks=50, performance=4.9, skills='Go, Microservices', team='API Team', experience_years=7)
	]

# Тест для проверки чтения CSV-файла
def test_read_csv():
	"""
	Тестирует функцию read_csv на корректность чтения данных из CSV-файла.
	"""
	sample_data = [
			{'name': 'John Doe', 'position': 'Backend Developer', 'completed_tasks': '45', 'performance': '4.8', 'skills': 'Python, Django', 'team': 'API Team', 'experience_years': '5'},
			{'name': 'Jane Smith', 'position': 'Frontend Developer', 'completed_tasks': '38', 'performance': '4.7', 'skills': 'React, TypeScript', 'team': 'Web Team', 'experience_years': '4'}
	]
	with open('test_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
			fieldnames = ['name', 'position', 'completed_tasks', 'performance', 'skills', 'team', 'experience_years']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerows(sample_data)
    
	result = read_csv('test_data.csv')
	assert len(result) == 2
	assert isinstance(result[0], Developer)
	assert result[0].name == 'John Doe'
	assert result[0].position == 'Backend Developer'
	assert result[0].performance == 4.8

# Тест для проверки обработки данных
def test_process_data(sample_data):
	"""
	Тестирует метод generate на корректность обработки данных.
	"""
	expected_result = [
			('Backend Developer', 4.85),
			('Frontend Developer', 4.7)
	]
	report_generator = PerformanceReport()
	result = report_generator.generate(sample_data)
	assert sorted(result) == sorted(expected_result)

# Тест для проверки вывода отчёта
def test_generate_report(capsys):
	"""
	Тестирует функцию generate_report на корректность вывода отчёта.
	"""
	sample_report = [
			('Backend Developer', 4.85),
			('Frontend Developer', 4.7)
	]
	generate_report(sample_report)
	captured = capsys.readouterr()
	assert 'Backend Developer' in captured.out
	assert '4.85' in captured.out
	assert 'Frontend Developer' in captured.out
	assert '4.7' in captured.out

# Тест для проверки параметризации
def test_process_data_param(sample_data):
	expected = [
			('Backend Developer', 4.85),
			('Frontend Developer', 4.7)
	]
	report_generator = PerformanceReport()
	result = report_generator.generate(sample_data)
	assert sorted(result) == sorted(expected)