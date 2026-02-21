from django.shortcuts import render, redirect
from .forms import StudyTaskForm
from .models import StudyTask
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    tasks = StudyTask.objects.filter(user=request.user)
    return render(request, "home.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = StudyTaskForm()
    return render(request, 'add_task.html', {'form': form})
