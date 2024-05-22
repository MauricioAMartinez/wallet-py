FROM python:3.9-slim

WORKDIR /app

# Copiar los archivos de la aplicación
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5001

# Comando para correr la aplicación
CMD ["python", "app.py"]
