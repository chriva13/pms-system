from django.contrib import admin
from django.urls import path
from pmsApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home"),
    path('login/', LoginView.as_view(template_name="registration/login.html", next_page="home"), name="login"),
    path('objectives/', ObjectivesView.as_view(), name="objectives"),
    path('targets/', TargetsView.as_view(), name="targets"),
    path('archievement/', ArchievementView.as_view(), name="archievement"),
    path('reports/', ReportsView.as_view(), name="reports"),
    path('indicators/', IndicatorsView.as_view(), name="indicators"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('forgotPassword/', ForgotPasswordView.as_view(), name="forgotPassword"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
