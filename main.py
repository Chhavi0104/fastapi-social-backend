from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

users = []
posts = []
app = FastAPI()

class UserCreate(BaseModel) :
    username : str
    password : str
    bio : Optional[str] = None
    pronouns : Optional[str] = None
    nickname : Optional[str] = None

class PostCreate(BaseModel) :
    user_id : int
    content : str

class PostUpdate(BaseModel) :
    content : str

@app.post('/users')
def add_user(user : UserCreate):
    user_id = len(users) + 1
    info = {'id': user_id, 'username': user.username, 'password': user.password, 'bio': user.bio, 'pronouns': user.pronouns, 'nickname': user.nickname}
    
    users.append(info)
    return {'message': 'User Created Successfully!'}

@app.get('/users')
def get_users():
    return users

@app.get('/users/{user_id}')
def get_user(user_id : int):
    for user in users:
        if user['id'] == user_id:
            return user
    
    raise HTTPException(status_code=404, detail='User not found')

@app.post('/posts')
def create_post(post : PostCreate):
    for user in users:
        if user['id'] == post.user_id:
            post_id = len(posts) + 1
            pos = {'post_id': post_id, 'user_id': post.user_id, 'content': post.content}
            
            posts.append(pos)

            return pos
        
    raise HTTPException(status_code=404, detail='User Not Found')
            
@app.get('/posts/{post_id}')
def get_post(post_id : int):
    for post in posts:
        if post['post_id'] == post_id:
            return post

    raise HTTPException(status_code=404, detail='Post Not Found')   

@app.get('/posts')
def get_posts():
    return posts
    
@app.put('/posts/{post_id}')
def update_post(post_id: int, post: PostUpdate):
    for pos in posts:
        if pos['post_id'] == post_id:
            pos['content'] = post.content

            return pos
        
    raise HTTPException(status_code=404, detail='Post Not Found')

@app.delete('/posts/{post_id}')
def delete_post(post_id: int):
    for pos in posts:
        if pos['post_id'] == post_id:
            posts.remove(pos)

            return {'message':'Post Deleted'}
        
    raise HTTPException(status_code=404, detail='Post Not Found')