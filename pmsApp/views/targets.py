from django.shortcuts import redirect, render
from pmsApp.forms import TargetForm
from pmsApp.models import Target


def add_target(request):
    if request.method == 'POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.save(commit=False)
            target.created_by = request.user
            target.save()
            return redirect('/targets')
        return render(request, 'interface/target-crud.html', {'form': form, 'action': 'add-target'})
    else:
        form = TargetForm()
        return render(request, 'interface/target-crud.html', {'form': form, 'action': 'add-target'})


def edit_target(request, pk):
    try:
        target = Target.objects.get(id=pk)
        if request.method == 'POST':
            form = TargetForm(request.POST, instance=target)
            if form.is_valid():
                target = form.save(commit=False)
                target.updated_by = request.user
                target.save()
                return redirect('/targets')
        form = TargetForm(instance=target)
        return render(
            request,
            'interface/target-crud.html',
            {
                'form': form,
                'target': target,
                'action': f'/edit-target/{target.id}'
            }
        )
    except Target.DoesNotExist:
        return redirect('/targets')
