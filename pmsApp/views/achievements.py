# views.py
from django.shortcuts import render, redirect

from pmsApp.forms import AchievementForm
from pmsApp.models import Achievement


def add_achievement(request):
    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.created_by = request.user
            achievement.save()
            return redirect('/achievements')
    else:
        form = AchievementForm()
    return render(request, 'interface/achievement-crud.html', {'form': form, 'action': 'add-achievement'})


def edit_achievement(request, pk):
    try:
        achievement = Achievement.objects.get(id=pk)
        if request.method == 'POST':
            form = AchievementForm(request.POST, instance=achievement)
            if form.is_valid():
                form.save()
                return redirect('/achievements')
        else:
            form = AchievementForm(instance=achievement)
        return render(request, 'interface/achievement-crud.html', {'form': form, 'action': f'/edit-achievement/{achievement.id}'})
    except Achievement.DoesNotExist:
        return redirect('/achievements')


def delete_achievement(request, pk):
    try:
        achievement = Achievement.objects.get(id=pk)
        if request.method == 'POST':
            achievement.delete()
            return redirect('/achievements')
        return render(request, 'interface/achievement_confirm_delete.html', {'achievement': achievement})
    except Achievement.DoesNotExist:
        return redirect('/achievements')
