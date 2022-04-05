from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pusher

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3454",
    "http://localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


pusher_client = pusher.Pusher(
  app_id='1372542',
  key='de4f43d4d2ef0b884d48',
  secret='bc4ea4e5fb1e2c85fea1',
  cluster='eu',
  ssl=True
)

@app.post("/api/test")
async def read_root(request: Request):
    texte = await request.json()
    print(texte['nom'])
    pusher_client.trigger('my-channel', 'my-event', {'message': texte['nom']})
    
@app.post("/api/draw")
async def draw_point(request: Request):
    print("Drawing request received")
    data = await request.json()
    pusher_client.trigger('my-channel', 'draw-point', data)

    