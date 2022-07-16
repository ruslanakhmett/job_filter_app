import time
import flask
import telebot
import logging.config
from random import randint
from parsers_and_bot.models import Vacancy, Global_Users
from django.core.management.base import BaseCommand
from .manual_parse_hh import go_parse_hh
from .manual_parse_sj import go_parse_sj
from logger_config import configuring_dict


logging.config.dictConfig(configuring_dict)
logger = logging.getLogger('app_logger')


class Command(BaseCommand):
    def handle(self, *args, **options):
        TOKEN = "1767277269:AAHra9hNFGHeE6qhttrG-s_h-HdGf3cH0IA"
        WEBHOOK_HOST = "80.87.198.203"
        WEBHOOK_PORT = 8443
        WEBHOOK_LISTEN = "0.0.0.0"
        WEBHOOK_SSL_CERT = "./resources/certs/webhook_cert.pem"
        WEBHOOK_SSL_PRIV = "./resources/certs/webhook_pkey.pem"
        WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
        WEBHOOK_URL_PATH = f"/{TOKEN}/"

        bot = telebot.TeleBot(TOKEN)
        server = flask.Flask(__name__)

        @server.route("/", methods=["GET", "HEAD"])
        def index():
            return ""

        @server.route(WEBHOOK_URL_PATH, methods=["POST"])
        def webhook():
            if flask.request.headers.get("content-type") == "application/json":
                json_string = flask.request.get_data().decode("utf-8")
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])
                return ""
            else:
                flask.abort(403)

        # старт, получаем chat_id, запускаем первый поиск
        @bot.message_handler(commands=["start"])
        def send_welcome(message):  # noqa F811
            user_name = message.text.split()[1]  # вытаскиваем имя юзера как оно есть на сайте
            try:
                Global_Users.objects.filter(name=user_name).update(
                    tg_chat_id=message.chat.id
                )  # устанавливаем связь имени и chatid телеги
                logger.info('tg_id OK')
            except Exception as error:
                logger.exception(error)

            for user in Global_Users.objects.all():
                if (
                    user_name == user.name
                    and user.tg_chat_id > 1
                    and user.tg_chat_id != message.chat.id
                ) or (
                    user.tg_chat_id > 1
                    and user.tg_chat_id == message.chat.id
                    and user_name != user.name
                ):
                    bot.send_message(
                        message.chat.id,
                        "Извините, но к одному Telegram аккаунту можно привязать только один аккаунт JobFIlter, работа не может быть продолжена.",
                    )
                    break
                else:
                    bot.send_message(
                        message.chat.id,
                        f"Здравствуйте {user_name}, это JobFilter бот.\n"
                        "Он поможет собирать в одном месте только интересующие Вас вакансии из разных источников.",
                    )
                    try:
                        user_set = Global_Users.objects.get(name=user_name)
                    except Exception as error:
                        logger.exception(error)

                    vacancy_name = user_set.vacancy_name
                    vacancy_name_durty = user_set.vacancy_name_durty
                    sity = user_set.sity
                    time_start_unix = user_set.start_when_unix
                    time_start = user_set.start_when
                    only_with_salary = user_set.only_with_salary
                    salary_max = user_set.salary_max
                    salary_min = user_set.salary_min

                    try:
                        go_parse_hh(
                            vacancy_name_durty,
                            user_name,
                            message.chat.id,
                            sity,
                            time_start,
                            only_with_salary,
                            salary_max,
                            salary_min,
                        )
                        logger.info('parsing hh OK')
                    except Exception as error:
                        logger.exception(error)

                    bot.send_message(
                        message.chat.id,
                        f"Начинаем поиск по вакансиям {user_set.vacancy_name} в городе {user_set.sity}.",
                    )
                    try:
                        go_parse_sj(
                            vacancy_name,
                            user_name,
                            message.chat.id,
                            sity,
                            time_start_unix,
                            only_with_salary,
                            salary_max,
                            salary_min,
                        )
                        logger.info('parsing sj OK')
                    except Exception as error:
                        logger.exception(error)

                    bot.send_message(
                        message.chat.id,
                        f"Нашли {Vacancy.objects.all().filter(tg_id=message.chat.id).count()} подходящих вакансий.",
                    )
                    bot.send_message(
                        message.chat.id,
                        "Вы можете воспользоваться командой /give_me для их просмотра.",
                    )
                    break

        # запуск поиска вручную
        @bot.message_handler(commands=["run_find"])
        def start_command(message):  # noqa F811
            bot.send_message(message.chat.id, "Ищем...")
            try:
                user_set = Global_Users.objects.get(tg_chat_id=message.chat.id)
            except Exception as error:
                logger.exception(error)

            user_name = user_set.name
            vacancy_name = user_set.vacancy_name
            vacancy_name_durty = user_set.vacancy_name_durty
            sity = user_set.sity
            time_start_unix = user_set.start_when_unix
            time_start = user_set.start_when
            only_with_salary = user_set.only_with_salary
            salary_max = user_set.salary_max
            salary_min = user_set.salary_min

            try:
                added_new_vac = go_parse_hh(
                    vacancy_name_durty,
                    user_name,
                    message.chat.id,
                    sity,
                    time_start,
                    only_with_salary,
                    salary_max,
                    salary_min,
                )  # берем так же return функции, там количество найденных за конкретный проход
                logger.info('parsing hh OK')
            except Exception as error:
                logger.exception(error)

            try:
                added_new_vac += go_parse_sj(
                    vacancy_name,
                    user_name,
                    message.chat.id,
                    sity,
                    time_start_unix,
                    only_with_salary,
                    salary_max,
                    salary_min,
                )
                logger.info('parsing sj OK')
            except Exception as error:
                logger.exception(error)

            if (
                added_new_vac
                == Vacancy.objects.all().filter(tg_id=message.chat.id).count()
            ):
                bot.send_message(
                    message.chat.id, f"Нашли {added_new_vac} подходящих вакансий"
                )
            elif added_new_vac == 0:
                bot.send_message(message.chat.id, "Пока ничего нового не нашлось")
            else:
                bot.send_message(
                    message.chat.id,
                    f"Добавили еще {added_new_vac}, для Вас есть {Vacancy.objects.all().filter(tg_id=message.chat.id).filter(is_shown = False).count()} непросмотренных вакансий",
                )

        # запрос вакансии
        @bot.message_handler(commands=["give_me"])
        def start_command(message):  # noqa F811
            try:    
                number_vax = (
                    Vacancy.objects.all()
                    .filter(tg_id=message.chat.id)
                    .filter(is_shown=False)
                    .count()
                )
            except Exception as error:
                logger.exception(error)

            if number_vax > 0:

                vac = (
                    Vacancy.objects.all()
                    .filter(tg_id=message.chat.id)
                    .filter(is_shown=False)[randint(0, number_vax - 1)]
                )

                bot.send_message(message.chat.id, vac.url)
                vac.is_shown = True
                vac.save()
            else:
                bot.send_message(message.chat.id, "В базе пусто")

        # показать, сколько вакансий в базе на данный момент
        @bot.message_handler(commands=["show_number"])
        def start_command(message):  # noqa F811
            try:
                number_vax = (
                    Vacancy.objects.all()
                    .filter(tg_id=message.chat.id)
                    .filter(is_shown=False)
                    .count()
                )
            except Exception as error:
                logger.exception(error)

            if number_vax > 0:
                bot.send_message(
                    message.chat.id, f"Есть {number_vax} непросмотренных вакансий")
            else:
                bot.send_message(message.chat.id, "В базе пусто")

        # очистка базы пользовательская
        @bot.message_handler(commands=["clean_base"])
        def start_command(message):  # noqa F811
            for vac in Vacancy.objects.filter(tg_id=message.chat.id):
                vac.delete()
            bot.send_message(message.chat.id, "База очищена")

        # очистка базы всей полностью, только для админа
        @bot.message_handler(commands=["clean_all"])
        def start_command(message):  # noqa F811
            for vac in Vacancy.objects.all():
                vac.delete()
            bot.send_message(message.chat.id, "Done")

        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(
            url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
            certificate=open(WEBHOOK_SSL_CERT, "r"),
        )
        server.run(
            host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True,
        )
