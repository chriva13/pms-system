from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from pmsApp.forms import IndicatorValueForm
from pmsApp.models import Indicator, IndicatorValue, Period


def add_periods():
    periods = Period.objects.all()
    if periods.count() == 0:
        periods = [f'20{f"0{n}" if n < 10 else n}/{f"0{n+1}" if n+1 < 10 else n+1}' for n in range(20, 50)]
        for p in periods:
            Period.objects.create(name=p)


def add_indicator_value(request, indicator_id):
    indicator = get_object_or_404(Indicator, id=indicator_id)
    add_periods()
    if request.method == 'POST':
        form = IndicatorValueForm(request.POST)
        if form.is_valid():
            indicator_value = form.save(commit=False)
            indicator_value.indicator = indicator
            indicator_value.created_by = request.user
            indicator_value.save()
            return redirect(f'/edit-indicator/{indicator.id}')
    else:
        form = IndicatorValueForm()
    return render(
        request,
        'interface/indicator-values-crud.html',
        {'form': form, 'indicator': indicator, 'action': 'add-value'
         }
    )


def edit_indicator_value(request, indicator_id, value_id):
    indicator = get_object_or_404(Indicator, id=indicator_id)
    indicator_value = get_object_or_404(IndicatorValue, id=value_id)
    if request.method == 'POST':
        form = IndicatorValueForm(request.POST, instance=indicator_value)
        if form.is_valid():
            indicator_value.updated_by = request.user
            form.save()
            return redirect(f'/edit-indicator/{indicator.id}')
    else:
        form = IndicatorValueForm(instance=indicator_value)
    return render(
        request,
        'interface/indicator-values-crud.html',
        {
            'form': form,
            'indicator': indicator,
            'action': f'/indicators/{indicator.id}/edit-value/{indicator_value.id}'
        }
    )


def get_indicator_values(request, indicator_id):
    # Fetch indicator values based on the selected indicator
    values = IndicatorValue.objects.filter(indicator_id=indicator_id).values('id', 'target_value')
    data = list(values)
    return JsonResponse(data, safe=False)
