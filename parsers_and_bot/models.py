from django.db import models

class Vacancy(models.Model):
    url = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    vac_id = models.IntegerField(primary_key=True)
    published_day = models.CharField(max_length=250, blank=True)
    published_time = models.CharField(max_length=250, blank=True)
    for_user = models.CharField(max_length=250, blank=True)
    tg_id = models.IntegerField()
    is_shown = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Global_Users(models.Model):
    name = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=250, blank=True)
    tg_chat_id = models.IntegerField()
    vacancy_name = models.CharField(max_length=250, blank=True)
    vacancy_name_durty = models.CharField(max_length=250, blank=True)
    sity = models.CharField(max_length=250, blank=True)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    start_when = models.CharField(max_length=250, default=True)
    only_with_salary = models.BooleanField(default=False)
    start_when_unix = models.IntegerField(default=0)

    def __str__(self):
        return self.name