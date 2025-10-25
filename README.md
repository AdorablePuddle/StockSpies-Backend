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
## II. Machine Learning Engine:
Before running the server, make sure to create a .env file containing:
```
OPENAI_API_KEY=<Insert Transfem Keysmashing Here>
```
With the appropriate OpenAI API key. The key must allow the usage of the gpt-4.1-mini model.

## III. Deployment:
To deploy the backend, first enter the settings.py and changes `DEBUG=False`.

Ideally, the backend should be moved to a production-ready WSGI or ASGI server. However, if you lack a server, simply running the server normally should still work. Other deployment requirements can be found in [the django documentation](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/#switch-away-from-manage-py-runserver).