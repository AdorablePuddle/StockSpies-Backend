# Stock Level Estimation / Backend App
## I. Installation
Installing requirements
```sh
pip install requirements.txt
```

Migrate database
```sh
python manage.py migrate
```

Run server:
```sh
python manage.py runserver
```
## II. Other complications
When using the backend, remember to follow the steps [here](https://pypi.org/project/qwen-api) to get the API key and cookie, replaced the one in .env with it.