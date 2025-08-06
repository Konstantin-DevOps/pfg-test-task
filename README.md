1. Set the access token in the .env file

2. Run commands sequentially

```
docker compose up -d --build

curl http://localhost:8000/fetch-dump

docker cp test-task-data/dump.sql db:/dump.sql

docker exec db psql -U postgres -d test_db -f /dump.sql

curl http://localhost:8000/fetch-alive-ssns
```