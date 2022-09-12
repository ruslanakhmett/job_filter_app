from django.db import models


class Global_Users(models.Model):
    for_user = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=250, blank=True)
    tg_chat_id = models.IntegerField()
    vacancy_name = models.CharField(max_length=250, blank=True)
    vacancy_name_durty = models.CharField(max_length=250, blank=True)
    sity = models.CharField(max_length=250, blank=True)
    salary_min = models.IntegerField(default=0)
    salary_max = models.IntegerField(default=0)
    start_when = models.CharField(max_length=250, blank=True)
    only_with_salary = models.BooleanField(default=False)
    start_when_unix = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    url = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    vac_id = models.IntegerField(primary_key=True)
    published_day = models.CharField(max_length=250, blank=True)
    published_time = models.CharField(max_length=250, blank=True)
    for_user = models.ForeignKey(Global_Users, related_name = 'For_user', on_delete=models.CASCADE)
    tg_id = models.IntegerField(default=0)
    is_shown = models.BooleanField(default=False)

    def __str__(self):
        return self.for_user

    class Meta:
        ordering = ['for_user']
