from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .forms import RegisterForm, StudyTaskForm
from .models import StudyTask, ActivityLog, LoginAttempt


# ==============================
# LANDING
# ==============================
def landing(request):
    return render(request, "landing.html")


# ==============================
# LOGIN (WITH IDS + LOCK SYSTEM)
# ==============================
def user_login(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        ip = request.META.get('REMOTE_ADDR')

        lock_time = timezone.now() - timedelta(minutes=2)

        recent_failed = LoginAttempt.objects.filter(
            username=username,
            success=False,
            timestamp__gte=lock_time
        )

        if recent_failed.count() >= 5:
            messages.error(request, "🚫 Account locked. Try again after 2 minutes.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            ActivityLog.objects.create(
                user=user,
                action=f"Logged in from IP {ip}"
            )

            LoginAttempt.objects.create(
                username=username,
                ip_address=ip,
                success=True
            )

            return redirect('dashboard')

        else:
            LoginAttempt.objects.create(
                username=username,
                ip_address=ip,
                success=False
            )

            failed_count = LoginAttempt.objects.filter(
                username=username,
                success=False,
                timestamp__gte=lock_time
            ).count()

            if failed_count >= 5:
                messages.error(request, "🚫 Too many attempts. Account locked for 2 minutes.")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# ==============================
# REGISTER
# ==============================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            ActivityLog.objects.create(
                user=user,
                action="Account created"
            )

            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


# ==============================
# DASHBOARD (NO ACTIVITY LOGS NOW)
# ==============================
@login_required(login_url='/login/')
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

    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    context = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress": progress,
    }

    return render(request, "home.html", context)


# ==============================
# ADD TASK
# ==============================
@login_required(login_url='/login/')
def add_task(request):
    if request.method == "POST":
        form = StudyTaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Created task: {task.title}"
            )

            return redirect("dashboard")
    else:
        form = StudyTaskForm()

    return render(request, "add_task.html", {"form": form})


# ==============================
# EDIT TASK
# ==============================
@login_required(login_url='/login/')
def edit_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)

    if request.method == "POST":
        form = StudyTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Updated task: {task.title}"
            )

            return redirect("dashboard")
    else:
        form = StudyTaskForm(instance=task)

    return render(request, "edit_task.html", {"form": form})


# ==============================
# DELETE TASK
# ==============================
@login_required(login_url='/login/')
def delete_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)

    ActivityLog.objects.create(
        user=request.user,
        action=f"Deleted task: {task.title}"
    )

    task.delete()
    return redirect("dashboard")


# ==============================
# COMPLETE TASK
# ==============================
@login_required(login_url='/login/')
def complete_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)

    task.completed = True
    task.completed_at = timezone.now()
    task.save()

    ActivityLog.objects.create(
        user=request.user,
        action=f"Completed task: {task.title}"
    )

    return redirect("dashboard")


# ==============================
# TOGGLE TASK
# ==============================
@login_required(login_url='/login/')
def toggle_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)

    task.completed = not task.completed

    if task.completed:
        task.completed_at = timezone.now()
        action_text = f"Completed task: {task.title}"
    else:
        task.completed_at = None
        action_text = f"Marked incomplete: {task.title}"

    task.save()

    ActivityLog.objects.create(
        user=request.user,
        action=action_text
    )

    return redirect("dashboard")


# ==============================
# PROFILE (NOW WITH ACTIVITY LOGS)
# ==============================
@login_required(login_url='/login/')
def profile(request):
    tasks = StudyTask.objects.filter(user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()

    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    # 🔥 ADDED HERE
    logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:10]

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "progress": progress,
        "logs": logs,
    }

    return render(request, "profile.html", context)


# ==============================
# LOGOUT
# ==============================
@login_required(login_url='/login/')
def user_logout(request):
    ActivityLog.objects.create(
        user=request.user,
        action="Logged out"
    )

    logout(request)
    return redirect('login')