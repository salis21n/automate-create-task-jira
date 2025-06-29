FROM python:alpine

WORKDIR /jira

COPY get-custom-field.py .

COPY .env .

RUN pip install requests python-dotenv

CMD ["sh", "-c", "python get-custom-field.py"]