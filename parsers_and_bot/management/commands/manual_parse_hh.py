import json
import logging.config

import requests

from parsers_and_bot.models import Vacancy

from .logger_config import configuring_dict

logging.config.dictConfig(configuring_dict)
logger = logging.getLogger('app_logger')


def go_parse_hh(
    vacancy_name_durty,
    user_name,
    tg_chat_id,
    sity,
    start_when,
    only_with_salary,
    salary_max,
    salary_min,
):

    if sity == "Москва":
        id_sity = 1
    elif sity == "Санкт-Петербург":
        id_sity = 2
    else:
        # формируем json с соответствиями город/id, может меняться, поэтому надо периодически обновлять, пока что обновляем каждый раз
        req = requests.get("https://api.hh.ru/areas")
        data = req.content.decode()
        req.close()

        jsObj = json.loads(data)
        with open("./resources/files_hh/files_hh/cityes_data.json", mode="w", encoding="utf8") as f:
            f.write(json.dumps(jsObj, ensure_ascii=False))

        # берем нужный id города в соответствии с введенным юзером названием для подстановки в запрос
        try:
            with open("./resources/files_hh/files_hhh/cityes_data.json", encoding="utf8") as f:
                jsonText = f.read()
        except FileNotFoundError as error:
            logger.exception(error)

        jsonObj = json.loads(jsonText)

        for item in jsonObj[0]["areas"]:
            for it in item["areas"]:
                if it["name"] == sity:
                    id_sity = it["id"]

    if salary_max + salary_min == 0:
        params = {
            "text": vacancy_name_durty,  # название вакансии (ключевые слова по имени вакансии в специальном формате для hh)
            "area": id_sity,  # берем id нужного города из заготовленного файла, для москвы и питера 1 и 2 для ускорения процесса
            "page": 0,  # ищем по первой странице и просматриваем 100 вакансиий, пока так
            "per_page": 100,
            "date_from": start_when,  # дата, свежее который мы иищем, выбирает юзер data/string
            "only_with_salary": only_with_salary,  # имещ только вакансии с указанной зарплатой true/false
        }
    else:
        params = {
            "text": vacancy_name_durty,  # название вакансии (ключевые слова по имени вакансии в специальном формате для hh)
            "area": id_sity,  # берем id нужного города из заготовленного файла, для москвы и питера 1 и 2 для ускорения процесса
            "page": 0,  # ищем по первой странице и просматриваем 100 вакансиий, пока так
            "per_page": 100,
            "date_from": start_when,  # дата, свежее который мы иищем, выбирает юзер data/string
            "only_with_salary": only_with_salary,  # имещ только вакансии с указанной зарплатой true/false
            "salary": (salary_max + salary_min) // 2,
        }

    req = requests.get("https://api.hh.ru/vacancies", params)
    data = req.content.decode()
    req.close()

    jsObj = json.loads(data)
    with open("./resources/files_hh/data_file.json", mode="w", encoding="utf8") as f:
        f.write(json.dumps(jsObj, ensure_ascii=False))

    try:
        with open("./resources/files_hh/data_file.json", encoding="utf8") as f:
            jsonText = f.read()
    except FileNotFoundError as error:
        logger.exception(error)

    jsonObj = json.loads(jsonText)

    count = 0

    for param in jsonObj["items"]:
        vac_id = int(param["id"])
        name = param["name"]
        url = param["alternate_url"]
        published_day = param["published_at"].split("T")[0]
        published_time = param["published_at"].split("T")[1].split("+")[0]

        try:
            Vacancy.objects.create(
                vac_id=vac_id,
                name=name,
                url=url,
                published_day=published_day,
                published_time=published_time,
                for_user=user_name,
                tg_id=tg_chat_id,
            )
            count += 1
        except Exception as error:
            logger.exception(error)
    return count
