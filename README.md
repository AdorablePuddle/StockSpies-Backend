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