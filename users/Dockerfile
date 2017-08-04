FROM python:3
CMD ["python", "/app/usersBackend.py"]
ADD libs.txt /app/libs.txt
RUN pip install -r /app/libs.txt
ADD usersBackend.py /app/usersBackend.py 