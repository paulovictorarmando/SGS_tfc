migrate:
	python manage.py makemigrations
	python manage.py migrate
run:
	uvicorn api.asgi:application --reload

add_admin:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_EMAIL=admin@gmail.com \
	DJANGO_SUPERUSER_PASSWORD=admin \
	python manage.py createsuperuser --noinput

venv:
	source venv/bin/activate
