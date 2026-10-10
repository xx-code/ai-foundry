alembic revision --autogenerate -m "create users and user_passwords"
alembic upgrade head

alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1   # annuler la dernière migration

run backend   

python -m uvicorn backend.presentation.api.main:app --app-dir src --env-file .env --log-level debug