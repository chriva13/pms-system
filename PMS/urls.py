from django.contrib import admin
from django.urls import path
from pmsApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home"),
    path('objectives/', ObjectivesView.as_view(), name="objectives"),
    path('targets/', TargetsView.as_view(), name="targets"),
    path('archievement/', ArchievementView.as_view(), name="archievement"),
    path('reports/', ReportsView.as_view(), name="reports"),
    path('indicators/', IndicatorsView.as_view(), name="indicators"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
