FROM python:3
CMD ["python", "/app/articlesBackend.py"]
ADD libs.txt /app/
RUN pip install -r /app/libs.txt
ADD articlesBackend.py /app/articlesBackend.py 