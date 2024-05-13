from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "interface/index.html"
    
    
class ObjectivesView(TemplateView):
    template_name = "interface/objectives.html"
    
class TargetsView(TemplateView):
    template_name = "interface/targets.html"

class ArchievementView(TemplateView):
    template_name = "interface/archievement.html"
    
class ReportsView(TemplateView):
    template_name = "interface/reports.html"
    
class IndicatorsView(TemplateView):
    template_name = "interface/indicators.html"
    

    
