import csv
import io 
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm

def is_admin(user):
    return user.is_superuser

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'crm/task_list.html', {'tasks': tasks})

@user_passes_test(is_admin)
def task_manage(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Проверьте, является ли пользователь администратором
    if not request.user.is_superuser:  # Или любое другое условие для админов
        return render(request, 'error_page.html', {'message': 'Access denied.'})  # Можно сделать страницу ошибки

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # Only calculate the deadline if it hasn't been set manually
            if not task.deadline:
                task.deadline = task.calculate_deadline()
            task.save()
            return redirect('task_list')  # Redirect after saving
    else:
        form = TaskForm(instance=task)

    return render(request, 'crm/task_manage.html', {'form': form, 'task': task})
