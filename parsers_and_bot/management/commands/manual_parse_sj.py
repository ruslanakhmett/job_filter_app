import requests, json, time, datetime
from parsers_and_bot.models import Vacancy
from decouple import config
import os


SECRET_KEY = config("SECRET_KEY_SJ")
SUPER_JOB_API = f'https://api.superjob.ru/2.33/vacancies/?keywords[srws][]=1&keywords[skwc][]=and&keywords[keys][]='
#super_job_api = 'https://api.superjob.ru/2.0/vacancies/?keywords[srws][]=1&keywords[skwc][]=and&keywords[keys][]=python программист'
headers = {'X-Api-App-Id': SECRET_KEY}


def go_parse_sj(vacancy_name, user_name, tg_chat_id, sity, start_when_unix, only_with_salary, salary_max, salary_min):

    payload = {
        'page': 0,
        'count': 100,
        'town': sity,
        'date_published_from': start_when_unix,
        'payment_from': salary_min,
        'payment_to': salary_max,
        'no_agreement': int(only_with_salary) # 1 не показывать без з/п
}

    req = requests.get(SUPER_JOB_API + vacancy_name, params=payload, headers=headers)
    data = req.content.decode()
    req.close()
    jsObj = json.loads(data)
    f = open('./resources/files_sj/data_file.json', mode='w', encoding='utf8')
    f.write(json.dumps(jsObj, ensure_ascii=False))
    f.close()
    time.sleep(1)

    f = open('./resources/files_sj/data_file.json', encoding='utf8')
    jsonText = f.read()
    f.close()
    jsonObj = json.loads(jsonText)

    count = 0

    for objects in jsonObj['objects']:
        #if vacancy_name.split()[1].upper() in objects['profession'].upper(): 
        vac_id = objects['id']
        name = objects['profession']
        url = objects['link']
        published_day = str(datetime.datetime.fromtimestamp(objects["date_published"])).split()[0]
        published_time = str(datetime.datetime.fromtimestamp(objects["date_published"])).split()[1]
        try:
            
            Vacancy.objects.create(
                vac_id=vac_id,
                name=name,
                url=url,
                published_day=published_day,
                published_time=published_time,
                for_user=user_name,
                tg_id=tg_chat_id)
            count += 1
        except:
            continue
    return count