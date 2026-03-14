from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from .forms import RegisterForm, StudyTaskForm
from .models import StudyTask


def landing(request):
    return render(request,"landing.html")


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(request,"register.html",{"form":form})


@login_required
def dashboard(request):

    query = request.GET.get("q")

    tasks = StudyTask.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()

    progress = 0

    if total_tasks > 0:
        progress = int((completed_tasks/total_tasks)*100)

    context = {
        "tasks":tasks,
        "total_tasks":total_tasks,
        "completed_tasks":completed_tasks,
        "progress":progress
    }

    return render(request,"home.html",context)


@login_required
def add_task(request):

    if request.method == "POST":
        form = StudyTaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect("dashboard")

    else:
        form = StudyTaskForm()

    return render(request,"add_task.html",{"form":form})


@login_required
def edit_task(request,task_id):

    task = get_object_or_404(
        StudyTask,
        id=task_id,
        user=request.user
    )

    if request.method == "POST":

        form = StudyTaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = StudyTaskForm(instance=task)

    return render(request,"edit_task.html",{"form":form})


@login_required
def delete_task(request,task_id):

    task = get_object_or_404(
        StudyTask,
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect("dashboard")


@login_required
def toggle_task(request,task_id):

    task = get_object_or_404(
        StudyTask,
        id=task_id,
        user=request.user
    )

    task.completed = not task.completed
    task.save()

    return redirect("dashboard")


@login_required
def profile(request):

    tasks = StudyTask.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()

    progress = 0

    if total_tasks > 0:
        progress = int((completed_tasks/total_tasks)*100)

    context = {
        "total_tasks":total_tasks,
        "completed_tasks":completed_tasks,
        "progress":progress
    }

    return render(request,"profile.html",context)