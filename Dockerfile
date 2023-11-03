FROM python:3.10

WORKDIR /app

COPY . ./app

RUN pip install -r requirements.txt
RUN pip install streamlit

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
