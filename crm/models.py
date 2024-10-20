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
    MAIN_CATEGORY_CHOICES = [
        ('improvement_department', 'Отдел благоустройства'),
        ('municipal_department', 'Отдел коммунального хозяйства'),
        ('entrepreneurship_department', 'Отдел по развитию предпринимательства'),
        ('infrastructure_department', 'Отдел инженерной и дорожной инфраструктуры'),
    ]

    SUBCATEGORY_CHOICES = {
        'improvement_department': [
            ('garbage_collection', 'Вывоз ТБО (либо уборка после)'),
            ('courtyard_cleaning', 'Уборка дворов (сан. очистка)'),
            ('waste_removal', 'Вывоз валки'),
            ('branch_removal', 'Вывоз веток'),
            ('irrigation_repair', 'Ремонт и содержание автополива'),
            ('street_cleaning', 'Уборка улиц (сан. очистка)'),
            ('sanitary_pruning', 'Санитарная обрезка'),
            ('tree_felling', 'Валка сухих/аварийных деревьев'),
        ],
        'municipal_department': [
            ('open_manhole', 'Открытый люк на дороге'),
            ('electricity_outage', 'Отключение электричества'),
            ('lighting_issue', 'Освещение не работает'),
            ('playground_repair', 'Ремонт детских элементов'),
        ],
        'entrepreneurship_department': [
            ('consultation', 'Консультация по компетенции'),
        ],
        'infrastructure_department': [
            ('other', 'Другие вопросы'),
        ]
    }

    title = models.CharField(max_length=255)
    description = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    performer = models.ForeignKey('Performers', related_name='performer', on_delete=models.SET_NULL, null=True, blank=True)
    observers = models.ForeignKey('Observers', related_name='observers', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('not_started', 'Не начато'), ('in_progress', 'В работе'), ('done', 'Завершено')])
    start_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, choices=MAIN_CATEGORY_CHOICES, blank=True)
    subcategory = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.deadline:
            self.deadline = self.calculate_deadline()
            super().save(update_fields=['deadline'])

    def calculate_deadline(self):
        days_to_add = {
            'open_manhole': 2,
            'electricity_outage': 2,
            'consultation': 2,
            'garbage_collection': 3,
            'courtyard_cleaning': 3,
            'waste_removal': 3,
            'branch_removal': 5,
            'irrigation_repair': 5,
            'lighting_issue': 5,
            'street_cleaning': 5,
            'sanitary_pruning': 10,
            'tree_felling': 10,
            'playground_repair': 10,
            'other': 5,
        }

        return self.created_at + timedelta(days=days_to_add.get(self.subcategory, 5))

    def __str__(self):
        return self.title
    

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if not self.deadline:
        self.deadline = self.calculate_deadline()
        super().save(update_fields=['deadline'])
