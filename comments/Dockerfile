FROM python:3
CMD ["python", "/app/commentsBackend.py"]
ADD libs.txt /app/
RUN pip install -r /app/libs.txt
ADD commentsBackend.py /app/commentsBackend.py