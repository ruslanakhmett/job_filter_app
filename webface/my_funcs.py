from parsers_and_bot.models import Vacancy


def clean_base(user_name):
    for vac in Vacancy.objects.all():
        if vac.for_user == user_name:
            vac.delete()