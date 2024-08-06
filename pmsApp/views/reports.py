from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import weasyprint
from pmsApp.forms import ReportForm
from pmsApp.models import ReportType, Report


def add_report_type():
    report_types = ReportType.objects.all()
    if report_types.count() == 0:
        ReportType.objects.create(name='Monitoring Plan ')
    if report_types.count() == 1:
        ReportType.objects.create(name='Achievement Report')


def add_report(request):
    add_report_type()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            return redirect('/reports')
    else:
        form = ReportForm()
    return render(request, 'reports/add_report.html', {'form': form, 'action': 'add-report'})


def plan_report_template(request, pk):
    report = Report.objects.get(id=pk)
    data = report.construct_monitoring_plan_report()

    # Render the HTML template with context data
    html_string = render_to_string(
        'reports/plan_template.html',
        {'data': data}, request=request
    )

    # Generate PDF from the rendered HTML with CSS for landscape orientation
    css = weasyprint.CSS(string='@page { size: A4 landscape; }')
    pdf_file = weasyprint.HTML(string=html_string).write_pdf(stylesheets=[css])
    # pdf_file = weasyprint.HTML(string=html_string).write_pdf()

    # Create a response to send the PDF to the browser
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'

    return response
    # return render(request, 'reports/plan_template.html', {'data': data})
