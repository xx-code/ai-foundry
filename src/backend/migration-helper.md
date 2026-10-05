alembic revision --autogenerate -m "create users and user_passwords"
alembic upgrade head

alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1   # annuler la dernière migration