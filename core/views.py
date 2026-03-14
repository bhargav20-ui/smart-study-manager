from django.shortcuts import render, redirect
from .forms import StudyTaskForm
from .models import StudyTask
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q

from django.contrib.auth import login
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()   # IMPORTANT: do not use commit=False
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

# Create your views here.
@login_required
def dashboard(request):
    query = request.GET.get('q')
    filter_status = request.GET.get('status')

    tasks = StudyTask.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
            )

    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()

    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0
    
    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress": progress,
    }
    return render(request, "home.html", context)

@login_required
def add_task(request):
    if request.method == 'POST':
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = StudyTaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(StudyTask, id=task_id, user=request.user)
        task.delete()
    return redirect('dashboard')

def landing(request):
    return render(request, "landing.html")


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')

@login_required
def profile(request):
    tasks = StudyTask.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress": progress,
    }
    return render(request, "profile.html", context)

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)

    if request.method == "POST":
        form = StudyTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudyTaskForm(instance=task)

    return render(request, "edit_task.html", {"form": form})