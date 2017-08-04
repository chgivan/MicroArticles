FROM python:3
CMD ["python", "/app/commentsBackend.py"]
ADD libs.txt authClient.py /app/
RUN pip install -r /app/libs.txt
ADD commentsBackend.py /app/commentsBackend.py