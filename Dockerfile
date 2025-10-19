# 🐍 Imagen base ligera y segura
FROM python:3.11-slim

# 🛠️ Variables de entorno (opcional para producción)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 📁 Directorio de trabajo
WORKDIR /app

# 📦 Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📁 Copiar el resto del proyecto
COPY . .

# 🔥 Exponer el puerto Flask
EXPOSE 5000

# 🚀 Comando de inicio
CMD ["python", "app.py"]
