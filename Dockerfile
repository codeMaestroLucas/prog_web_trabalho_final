FROM python:3.11.9

WORKDIR /app/back

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
# RUN cd back

# CMD ["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]

CMD ["uvicorn", "main:app", "--reload"]