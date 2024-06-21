from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from pmsApp.forms import ObjectiveForm
from pmsApp.models import Objective


def add_objective(request):
    if request.method == 'POST':
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.created_by = request.user
            objective.save()
            return redirect('/objectives')

        return render(request, 'interface/objective-crud.html', {'form': form, 'action': 'add-objective'})
    else:
        form = ObjectiveForm()
        return render(request, 'interface/objective-crud.html', {'form': form, 'action': 'add-objective'})


def edit_objective(request, pk):
    try:
        objective = Objective.objects.get(id=pk)
        if request.method == 'POST':
            form = ObjectiveForm(request.POST, instance=objective)

            if form.is_valid():
                form.save()
                return redirect('/objectives')

        form = ObjectiveForm(instance=objective)
        return render(
            request,
            'interface/objective-crud.html',
            {
                'form': form,
                'objective': objective,
                'action': f'/edit-objective/{objective.id}'
            }
        )
    except Objective.DoesNotExist:
        return redirect('/objectives')


def delete_objective(request, pk):
    if request.method == 'POST' and request.is_ajax():
        objective = get_object_or_404(Objective, pk=pk)
        objective.delete()
        return JsonResponse({'message': 'Objective deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

