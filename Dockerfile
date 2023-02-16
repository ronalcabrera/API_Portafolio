FROM tiangolo/uvicorn-gunicorn-fastapi

RUN PIP INSTALL Jinja2

EXPOSE 80

COPY ./app /app