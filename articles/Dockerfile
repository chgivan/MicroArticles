FROM python:3
CMD ["python", "/app/articlesBackend.py"]
ADD libs.txt authClient.py /app/
RUN pip install -r /app/libs.txt
ADD articlesBackend.py /app/articlesBackend.py 