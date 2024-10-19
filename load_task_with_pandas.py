import os
import pandas as pd
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings') 
django.setup()

from crm.models import Task, Performers, Observers
from django.contrib.auth.models import User

def load_tasks_from_csv(csv_file_path):
    if not os.path.isfile(csv_file_path):
        print(f"File {csv_file_path} does not exist.")
        return

    # Чтение CSV файла с указанием разделителя и игнорированием проблемных строк
    try:
        df = pd.read_csv(csv_file_path, sep=';', encoding='cp1251', on_bad_lines='warn')  
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, sep=';', encoding='ISO-8859-1', on_bad_lines='warn')  

    # Проверка на количество строк и столбцов в DataFrame
    print(f"DataFrame loaded with {df.shape[0]} rows and {df.shape[1]} columns.")

    expected_columns = ['title', 'description', 'category']  
    for column in expected_columns:
        if column not in df.columns:
            print(f"Missing column in CSV: {column}")
            return

    df['deadline'] = pd.to_datetime(df['deadline'], format='%d.%m.%Y %H:%M', errors='coerce')
    df['created_at'] = pd.to_datetime(df['created_at'], format='%d.%m.%Y %H:%M', errors='coerce')
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d.%m.%Y %H:%M', errors='coerce')
    df['updated_at'] = pd.to_datetime(df['updated_at'], format='%d.%m.%Y %H:%M', errors='coerce')
    df['closed_at'] = pd.to_datetime(df['closed_at'], format='%d.%m.%Y %H:%M', errors='coerce')
    df['last_activity'] = pd.to_datetime(df['last_activity'], format='%d.%m.%Y %H:%M', errors='coerce')

    # Итерация по DataFrame и создание экземпляров Task
    for _, row in df.iterrows():
        task = Task(
            title=row['title'],
            description=row['description'],
            category=row['category'],
            status=row['status'],
            last_activity=row['last_activity'],
            deadline=row['deadline'],
            created_at=row['created_at'],
            start_date=row['start_date'],
            updated_at=row['updated_at'],
            closed_at=row['closed_at'],
            creator=User.objects.first()
        )
        performer = Performers(
            name=row['performer']
        )
        observers = Observers(
            name=row['observers']
        )
        task.save()
        performer.save()
        observers.save()
        print(f'Task "{task.title}" added successfully.')

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python load_task_with_pandas.py <csv_file_path>")
    else:
        csv_file_path = sys.argv[1]
        load_tasks_from_csv(csv_file_path)