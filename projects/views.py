from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .forms import ProjectForm, ReviewForm


def projects(request):
    proj_objects = Project.objects.all()
    context = {'projects': proj_objects}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    proj_object = Project.objects.get(id=pk)
    form = ReviewForm()
    tags = proj_object.tags.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = proj_object
        review.owner = request.user.profile
        review.save()
        proj_object.get_like_count
        messages.success(request, 'Ваш отзыв был успешно добавлен!')
        return redirect('project', pk=proj_object.id)
    return render(request, 'projects/single-project.html', {'project': proj_object, 'tags': tags, 'form': form})


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            _project = form.save(commit=False)
            _project.owner = profile
            _project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    _project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=_project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=_project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    _project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        _project.delete()
        return redirect('account')
    context = {'object': _project}
    return render(request, 'delete_object.html', context)

