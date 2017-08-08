set PORT=8080
set DEBUG=true
set DB_HOST=192.168.99.100
set DB_USER=users
set DB_PASSWORD=1234
set DB_DATABASE=usersDB

python usersBackend.py

docker run --name userdb -p "5432:5432" -e POSTGRES_USER=users -e POSTGRES_DB=usersDB -e POSTGRES_PASSWORD=1234 -d postgres
