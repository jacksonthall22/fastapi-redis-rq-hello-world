# fastapi-redis-rq-hello-world
Simple "hello world" server using FastAPI, Docker for horizontal scaling, Redis for memory sharing between workers, and RQ to manage task queuing and routing.

## Test
```
git clone git@github.com:jacksonthall22/fastapi-redis-rq-hello-world.git
cd fastapi-redis-rq-hello-world
docker compose up -d
curl -X POST http://127.0.0.1:8000/new1
```