JobFilter is my first pet-project as a python developer.

It is a telegram bot (flask + pyTelegramBotAPI) that has a web interface (django + nginx + gunicorn) for registration, authorisation and setting search parameters.

The program parses several of the most popular sites with vacancies according to the specified parameters and collects them in database (postgre) for delivery to the user.

The user can request and view vacancies in his database, run a search manually and clear the database directly from telegram.