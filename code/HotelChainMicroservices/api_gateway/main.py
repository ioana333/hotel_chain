from fastapi import FastAPI, Request, Response
import httpx

SERVICE_MAP = {
    "hotel": {
        "url": "http://127.0.0.1:8001",
        "prefix": "/api/hotels"
    },
    "room": {
        "url": "http://127.0.0.1:8002",
        "prefix": "/api/rooms"
    },
    "reservation": {
        "url": "http://127.0.0.1:8003",
        "prefix": "/api/reservations"
    },
    "review": {
        "url": "http://127.0.0.1:8004",
        "prefix": "/api/reviews"
    },
    "user": {
        "url": "http://127.0.0.1:8005",
        "prefix": "/api/users"
    },
    "notification": {
        "url": "http://127.0.0.1:8006",
        "prefix": "/api/notifications"
    }
}

app = FastAPI(title='HotelChainAPIGateway', version='1.0.0')

@app.get('/health')
def health():
    return {'service': 'HotelChainAPIGateway', 'status': 'ok', 'microservices': list(SERVICE_MAP)}

async def proxy(service_key: str, path: str, request: Request):
    if service_key not in SERVICE_MAP:
        return Response(content='Unknown service', status_code=404)
    target = SERVICE_MAP[service_key]['url'] + SERVICE_MAP[service_key]['prefix']
    if path:
        target += '/' + path
    params = dict(request.query_params)
    body = await request.body()
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.request(request.method, target, params=params, content=body, headers=headers)
    return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get('content-type'))

@app.api_route('/{service_key}', methods=['GET','POST','PUT','DELETE','PATCH'])
async def proxy_root(service_key: str, request: Request):
    return await proxy(service_key, '', request)

@app.api_route('/{service_key}/{path:path}', methods=['GET','POST','PUT','DELETE','PATCH'])
async def proxy_path(service_key: str, path: str, request: Request):
    return await proxy(service_key, path, request)
