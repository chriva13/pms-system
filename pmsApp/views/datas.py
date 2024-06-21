# views.py
from django.shortcuts import render, redirect, get_object_or_404
from pmsApp.forms import DataSourceForm, DataCollectionMethodForm
from pmsApp.models import DataSource, DataCollectionMethod


def data_list(request):
    data_sources = DataSource.objects.all()
    data_collection_methods = DataCollectionMethod.objects.all()
    return render(request, 'interface/datas.html', {
        'data_sources': data_sources,
        'data_collection_methods': data_collection_methods,
    })


# DataSource views
def add_data_source(request):
    if request.method == 'POST':
        form = DataSourceForm(request.POST)
        if form.is_valid():
            data_source = form.save(commit=False)
            data_source.created_by = request.user
            data_source.save()
            return redirect('datas')
    else:
        form = DataSourceForm()
    return render(request, 'interface/data-source-crud.html', {'form': form, 'action': '/data/add-source/'})


def edit_data_source(request, pk):
    data_source = get_object_or_404(DataSource, pk=pk)
    if request.method == 'POST':
        form = DataSourceForm(request.POST, instance=data_source)
        if form.is_valid():
            form.save()
            return redirect('datas')
    else:
        form = DataSourceForm(instance=data_source)
    return render(request, 'interface/data-source-crud.html', {'form': form, 'action': f'/data/edit-source/{data_source.id}/'})


def delete_data_source(request, pk):
    data_source = get_object_or_404(DataSource, pk=pk)
    if request.method == 'POST':
        data_source.delete()
        return redirect('datas')
    return render(request, 'interface/confirm_delete.html', {'object': data_source, 'type': 'Data Source'})


# DataCollectionMethod views
def add_data_collection_method(request):
    if request.method == 'POST':
        form = DataCollectionMethodForm(request.POST)
        if form.is_valid():
            data_collection_method = form.save(commit=False)
            data_collection_method.created_by = request.user
            data_collection_method.save()
            return redirect('datas')
    else:
        form = DataCollectionMethodForm()
    return render(request, 'interface/data-collection-crud.html', {'form': form, 'action': '/data/add-method/'})


def edit_data_collection_method(request, pk):
    data_collection_method = get_object_or_404(DataCollectionMethod, pk=pk)
    if request.method == 'POST':
        form = DataCollectionMethodForm(request.POST, instance=data_collection_method)
        if form.is_valid():
            form.save()
            return redirect('datas')
    else:
        form = DataCollectionMethodForm(instance=data_collection_method)
    return render(request, 'interface/data-collection-crud.html', {'form': form, 'action': '/data/edit-method/<int:pk>/'})


def delete_data_collection_method(request, pk):
    data_collection_method = get_object_or_404(DataCollectionMethod, pk=pk)
    if request.method == 'POST':
        data_collection_method.delete()
        return redirect('datas')
    return render(request, 'interface/confirm_delete.html', {'object': data_collection_method, 'type': 'Data Collection Method'})
