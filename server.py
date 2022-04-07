from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pusher

import sqlite3



def setup_database(): # We build the database
    conn = sqlite3.connect('pixel_base.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pixel(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        x INTEGER,
        y INTERGER,
        color VARCHAR(7)
    )
    """)
    conn.commit()
    # cursor = conn.cursor()
    # cursor.execute("""
    # DROP TABLE pixel
    # """)
    # conn.commit()
    conn.close()
    
# setup_database()
    
def insert_color(x, y, color): # We insert the color in the database
    conn = sqlite3.connect('pixel_base.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT x, y, color FROM pixel WHERE x = ? AND y = ?;""", (x, y))
    pixel = cursor.fetchone()
    # We start to check if the pixel are not already in the database
    print(pixel)
    if pixel == None: # It doesn't exist, we insert it
        cursor.execute("""
         INSERT INTO pixel(x, y, color) VALUES (?, ?, ?)
         """, (x, y, color))
        print('Inserted')
    else: # It exists, we update it
        cursor.execute("""
                      UPDATE pixel SET color = ? WHERE x = ? AND y = ?; 
                       """, (color, x, y))
        print('Updated')
    
    conn.commit()
    conn.close()
    
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
    # We save it in the database
    insert_color(data['x'], data['y'], data['color'])
    # Then we send it to all the other clients
    pusher_client.trigger('my-channel', 'draw-point', data)

@app.get("/api/get_all")
async def get_all(request: Request): # We get all the pixels that we will send to all the users at the connexion
    conn = sqlite3.connect('pixel_base.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT x, y, color FROM pixel;""")
    pixels = cursor.fetchall()
    conn.close()
    return {'pixels': pixels}