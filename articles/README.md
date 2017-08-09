set USERS_HOST=localhost:8080
set DB_HOST=192.168.99.100
set DEBUG=true
set PORT=8081

python articlesBackend.py

docker run --name mongodb -p "27017:27017" -d mongo


