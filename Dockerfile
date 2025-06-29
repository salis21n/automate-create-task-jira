FROM python:alpine

WORKDIR /jira

COPY . .

RUN pip install pandas requests openpyxl

CMD ["sh", "-c", "python jira.py data.csv"]