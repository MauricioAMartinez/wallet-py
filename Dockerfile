FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

ENV FLASK_ENV=development

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
