from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Database Connection
# Only start server if database is connected
while True:
    try:
        # instantiate conn object
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres' ,password = 'test', cursor_factory=RealDictCursor)
        # Execute sql commands
        cursor = conn.cursor()
        print("Database successfully connected!")
        break
    except Exception as error:
        print("failed to connect to datebase")
        print(error)
        time.sleep(2)

app = FastAPI()

# Schema model for requests
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
'''
my_posts = [{"title": "title of post", "content": "content of post", "id": 123},
            {"title": "food", "content": "i like pizza", "id": 1}]

# API Implementation
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i'''

@app.get("/")
def root():
    return {"Message":"Welcome to my API!!!"}

@app.get("/posts")
def get_posts():
    # command
    cursor.execute("""SELECT * FROM posts""")
    # execute command and get data from database
    posts = cursor.fetchall()
    return {"data":posts}

'''@app.get("/post/latest")
def get_lastest_post():
    post = my_posts[len(my_posts)-1]
    return {"Post detail": post}'''

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    # command
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id))
    # execute command and get data from database
    posts = cursor.fetchone()
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} not found" )
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # SQL INSERT command
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    # commit changes to database
    conn.commit()
    return{"data": new_post}

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING * ''', str(id))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with {id} not found')

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'post with {id} not found')
    
    return {"data:": updated_post}