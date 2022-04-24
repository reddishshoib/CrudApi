from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange  
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published:bool = True

my_posts=[{"title":"title of post 1","content":"Content of Post 1","id": 1},
          {"title":"title of post 2","content":"Content of Post 2","id": 2},
          {"title":"title of post 3","content":"Content of Post 3","id": 3}  ]

while True:
    try:
        conn = psycopg2.connect(host='<hostname>',database='<databasename>',user='username',
            password='<password>',cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("The error : ",error)
        time.sleep(2)




def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p

def fin_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i

@app.get("/") 
async def root():
    return {"message":"Good World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from products""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts }

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def creat_post(post: Post ):
    cursor.execute("""insert into posts(title,content,published) values(%s, %s, %s)
    returning * """,(post.title, post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    # post_dict = new_post.dict()
    # post_dict['id']= randrange(0,1000000)
    # # print(new_post.rating, new_post.content ) 
    # my_posts.append(post_dict)
    return {"data": new_post}
    # return {"message":f"title: {payLoad['title']} content: {payLoad['content']}"}

#Title str, content str

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int,response : Response):
    cursor.execute("""select * from posts where id = %s""",(str(id)))
    test_post = cursor.fetchone()
    print(test_post)
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} not found")
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"MESSAGE ": f"post with id {id} not found"}
    return {"post details ": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""delete from posts where id = %s returning *   """,(str(id)))
    delete_posts = cursor.fetchone()
    conn.commit()

    if delete_posts == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'Post with id does not exiest')
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post : Post):
    cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""",
    (post.title,post.content,post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f'Post with id does not exiest')

    # post_dict= post.dict()
    # post_dict['id']=id
    # my_posts[index]= post_dict
    return {'data':updated_post}
