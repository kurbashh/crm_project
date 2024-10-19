from django.urls import path
from .views import task_list, task_manage

urlpatterns = [
    path('', task_list, name='task_list'),
    path('manage/<int:task_id>/', task_manage, name='task_manage'),
]