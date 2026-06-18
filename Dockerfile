FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 2718 8888

# Por padrão sobe o Marimo (você pode mudar para jupyter)
CMD ["marimo", "run", "app.py", "--host", "0.0.0.0", "--port", "2718"]