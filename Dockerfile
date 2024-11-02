# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo los archivos necesarios para instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda la carpeta del proyecto Django al contenedor
COPY text_analysis /app/text_analysis
COPY text_analysis_service /app/text_analysis_service
COPY manage.py /app/
COPY .env /app/

# Configura variables de entorno
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=text_analysis_service.settings

# Expone el puerto que usará Django
EXPOSE 8000

# Ejecuta migraciones y corre el servidor de Django
CMD ["sh", "-c", "python /app/manage.py migrate && python /app/manage.py runserver 0.0.0.0:8000"]
