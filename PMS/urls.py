from django.contrib import admin
from django.urls import path
from pmsApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

from pmsApp.views.reports import plan_report_template, add_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home"),
    path('login/', LoginView.as_view(template_name="registration/login.html", next_page="home"), name="login"),
    path('login-request', login_request, name="login-request"),

    # Objective APIs
    path('objectives/', ObjectivesView.as_view(), name="objectives"),
    path('add-objective', add_objective, name="add-objective"),
    path('edit-objective/<str:pk>', edit_objective, name="edit-objective"),
    path('delete-objective/<int:pk>/', delete_objective, name='delete-objective'),

    # Targets APIs
    path('targets/', TargetsView.as_view(), name="targets"),
    path('add-target', add_target, name="add-target"),
    path('edit-target/<str:pk>', edit_target, name="edit-target"),

    # Indicators APIs
    path('indicators/', IndicatorsView.as_view(), name="indicators"),
    path('add-indicator', add_indicator, name="add-indicator"),
    path('edit-indicator/<str:pk>', edit_indicator, name="edit-indicator"),

    path('indicators/<int:indicator_id>/add-value', add_indicator_value, name='add-indicator-value'),
    path('indicators/<int:indicator_id>/edit-value/<int:value_id>', edit_indicator_value, name='edit-indicator-value'),
    path('indicators/<int:indicator_id>/values', IndicatorsValueView.as_view(), name='indicator-value-list'),

    # Achievements APIs
    path('achievements/', AchievementView.as_view(), name="achievements"),
    path('add-achievement', add_achievement, name='add-achievement'),
    path('edit-achievement/<str:pk>', edit_achievement, name='edit-achievement'),

    # Datas APIs
    path('datas/', DatasView.as_view(), name='datas'),
    path('data/add-source', add_data_source, name='add_data_source'),
    path('data/edit-source/<int:pk>', edit_data_source, name='edit_data_source'),
    path('data/delete-source/<int:pk>', delete_data_source, name='delete_data_source'),
    path('data/add-method', add_data_collection_method, name='add_data_collection_method'),
    path('data/edit-method/<int:pk>', edit_data_collection_method, name='edit_data_collection_method'),
    path('data/delete-method/<int:pk>', delete_data_collection_method, name='delete_data_collection_method'),


    path('reports/', ReportsView.as_view(), name="reports"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('forgotPassword/', ForgotPasswordView.as_view(), name="forgotPassword"),

    # Reports Resources
    path('add-report', add_report, name='plan_report_template'),
    path('report/template/plan/<str:pk>', plan_report_template, name='plan_report_template')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
