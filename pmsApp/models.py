from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from pmsApp.manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    USER_CHOICES = (
        ("admin", "admin"),
        ("hod", "hod"),
        ("manager", "institute_manager"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    user_type = models.CharField(max_length=30, choices=USER_CHOICES)

    # Remove the username field
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'user_type', 'contact']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Objective(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    service_output = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Target(models.Model):

    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DataSource(models.Model):
    name: str = models.CharField(max_length=255)  # not necessary to add type hint

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DataCollectionMethod(models.Model):
    name = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Indicator(models.Model):
    WORDS, NUMBER = 'words', 'number'
    ANNUALLY, QUARTERLY, MONTHLY = 'Annually', 'Quarterly', 'Monthly'

    TYPE_CHOICES = (
        (WORDS, 'Words'),
        (NUMBER, 'Number')
    )

    FREQUENCY_CHOICES = (
        (WORDS, 'Annually'),
        (QUARTERLY, 'Quarterly'),
        (MONTHLY, 'Monthly')
    )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)

    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
    data_collection_method = models.ForeignKey(DataCollectionMethod, on_delete=models.CASCADE)

    type = models.CharField(choices=TYPE_CHOICES, max_length=255)
    frequency = models.CharField(choices=FREQUENCY_CHOICES, max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Period(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IndicatorValue(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='+')
    target_value = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.period} - Value: {self.target_value}'


class Achievement(models.Model):
    indicator_value = models.ForeignKey(IndicatorValue, on_delete=models.CASCADE)
    target_value = models.CharField(max_length=255)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReportType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Report(models.Model):
    type = models.ForeignKey(ReportType, on_delete=models.CASCADE)
    indicator_period_start = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='+')
    indicator_period_end = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='+')

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

    def construct_monitoring_plan_report(self):
        # get periods
        periods = self.__obtain_periods_list()
        print(periods)

        # get objectives
        objective_data = []
        objectives = Objective.objects.all()
        for i in range(len(objectives)):
            targets = self.__obtain_objective_targets(periods[0], objectives[i])
            objective_data.append({
                'sn': i + 1,
                'objective': objectives[i],
                'targets': targets,
            })

        return {
            'periods': periods,
            'period_length': len(periods),
            'total_span': len(periods) + 10,
            'initial_period': periods[0],
            'objectives': objective_data
        }

    def __obtain_objective_targets(self, initial_period: Period, objective: Objective):
        objective_data = []

        targets = Target.objects.filter(objective=objective)
        for i in range(targets.count()):
            indicators = Indicator.objects.filter(target=targets[i])
            if indicators.count() > 0:
                objective_data.append({
                    'sn': i + 1,
                    'target': targets[i],
                    'indicators': [
                        {
                            'sn': n + 1,
                            'initial_value': self.__get_indicator_value(initial_period, indicators[n]),
                            'indicator': indicators[n]} for n in range(len(indicators))]
                })

        return objective_data


    def __get_indicator_value(self, period: Period, indicator: Indicator):
        try:
            indicator_value = IndicatorValue.objects.get(indicator=indicator, period=period)
            return indicator_value.target_value
        except IndicatorValue.DoesNotExist:
            return 0

    def __obtain_periods_list(self):
        return [Period.objects.get(id=n) for n in range(self.indicator_period_start.id, self.indicator_period_end.id)]

