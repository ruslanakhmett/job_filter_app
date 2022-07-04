import requests, json, time, datetime
from django.core.management.base import BaseCommand
from hh_parser.models import Vacancy, Global_Users


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Global_Users.objects.all():    
            params = {
                'text': str(item.vacancy_name), 
                'area': 1, 
                'page': 0,
                'per_page': 100,
                'date_from': '2021-09-21'}

            req = requests.get('https://api.hh.ru/vacancies', params)
            data = req.content.decode()
            req.close()
            
            jsObj = json.loads(data)
            f = open('files_hh/data_file.json', mode='w', encoding='utf8')
            f.write(json.dumps(jsObj, ensure_ascii=False))
            f.close()
            time.sleep(3)
            
            f = open('files_hh/data_file.json', encoding='utf8')
            jsonText = f.read()
            f.close()
            jsonObj = json.loads(jsonText)
    
            count = 0
            today = datetime.datetime.today()
            for param in jsonObj['items']:
                
                vac_id = int(param['id'])
                name = param['name']
                url = param['alternate_url']
                published_day= param['published_at'].split('T')[0]
                published_time = param['published_at'].split('T')[1].split('+')[0]
    
                try:
                    print(vac_id, name)
                    Vacancy.objects.create(
                        vac_id=vac_id,
                        name=name,
                        url=url,
                        published_day=published_day,
                        published_time=published_time,
                        for_user=item.name,
                        tg_id=item.tg_chat_id)
                    count += 1
                    print(f'Added {name}')
                except:
                    print('Already exists')
            print( 'job complete', count, today.strftime("%Y-%m-%d %H:%M:%S"))