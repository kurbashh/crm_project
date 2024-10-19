from datetime import timedelta
from django.db import models


# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Performers(models.Model):
    name = models.CharField(max_length=500)


    def __str__(self):
        return self.name

class Observers(models.Model):
    name = models.CharField(max_length=500)


    def __str__(self):
        return self.name


class Task(models.Model):
    TAG_CHOICES = [
        ('open_manhole', 'Открытый люк на дороге'),
        ('electricity_outage', 'Отключение электричества'),
        ('consultation', 'Консультация по компетенции'),
        ('garbage_collection', 'Вывоз ТБО (либо уборка после)'),
        ('courtyard_cleaning', 'Уборка дворов (сан. очистка)'),
        ('waste_removal', 'Вывоз валки'),
        ('branch_removal', 'Вывоз веток'),
        ('irrigation_repair', 'Ремонт и содержание автополива'),
        ('lighting_issue', 'Освещение не работает'),
        ('street_cleaning', 'Уборка улиц (сан. очистка)'),
        ('sanitary_pruning', 'Санитарная обрезка'),
        ('tree_felling', 'Валка сухих/аварийных деревьев'),
        ('playground_repair', 'Ремонт детских элементов'),
        ('other', 'Другие вопросы'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    performer = models.ForeignKey(Performers, related_name='performer', on_delete=models.SET_NULL, null=True, blank=True)
    observers = models.ForeignKey(Observers, related_name='observers', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('not started', 'Не начато'), ('in progress', 'В работе'), ('done', 'Завершено')])
    start_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=TAG_CHOICES, blank=True)

    def str(self):
        return self.title

    def calculate_deadline(self):
        days_to_add = {
            'open_manhole': 2,  # Открытый люк на дороге – 2 рабочих дня
            'electricity_outage': 2,  # Отключение электричества – 2 рабочих дня
            'consultation': 2,  # Консультация по компетенции – 2 рабочих дня
            'garbage_collection': 3,  # Вывоз ТБО (либо уборка после) – 3 рабочих дня
            'courtyard_cleaning': 3,  # Уборка дворов (сан. очистка) – 3 рабочих дня
            'waste_removal': 3,  # Вывоз валки – 3 рабочих дня
            'branch_removal': 5,  # Вывоз веток – 5 рабочих дня
            'irrigation_repair': 5,  # Ремонт и содержание автополива – 5 рабочих дня
            'lighting_issue': 5,  # Освещение не работает – 5 рабочих дня
            'street_cleaning': 5,  # Уборка улиц (сан. очистка) – 5 рабочих дня
            'sanitary_pruning': 10,  # Санитарная обрезка – 10 рабочих дня
            'tree_felling': 10,  # Валка сухих/аварийных деревьев – 10 рабочих дня
            'playground_repair': 10,  # Ремонт детских элементов – 10 рабочих дня
            'other': 5,  # Другие вопросы – 5 рабочих дня
        }

        return self.created_at + timedelta(days=days_to_add.get(self.category, 5))
    

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if not self.deadline:
        self.deadline = self.calculate_deadline()
        super().save(update_fields=['deadline'])
