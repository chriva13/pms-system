from django.shortcuts import redirect, render
from pmsApp.forms import IndicatorForm
from pmsApp.models import Indicator, IndicatorValue


def add_indicator(request):
    if request.method == 'POST':
        form = IndicatorForm(request.POST)
        if form.is_valid():
            indicator = form.save(commit=False)
            indicator.created_by = request.user
            indicator.save()
            return redirect('/indicators')
        return render(request, 'interface/indicator-crud.html', {'form': form, 'action': 'add-indicator'})
    else:
        form = IndicatorForm()
        return render(request, 'interface/indicator-crud.html', {'form': form, 'action': 'add-indicator'})


def edit_indicator(request, pk):
    try:
        indicator = Indicator.objects.get(id=pk)
        if request.method == 'POST':
            form = IndicatorForm(request.POST, instance=indicator)
            if form.is_valid():
                indicator = form.save(commit=False)
                indicator.updated_by = request.user
                indicator.save()
                return redirect('/indicators')
        form = IndicatorForm(instance=indicator)
        return render(
            request,
            'interface/indicator-crud.html',
            {
                'form': form,
                'indicator': indicator,
                'values': IndicatorValue.objects.filter(indicator=indicator),  # Get all indicators
                'action': f'/edit-indicator/{indicator.id}'
            }
        )
    except Indicator.DoesNotExist:
        return redirect('/indicators')
