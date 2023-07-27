
from app import schema
import pytest

def test_get_all_posts(auth_client, create_test_posts):
    res = auth_client.get('/posts/')
    def validate_post(post):
        return schema.PostVote(**post)
    
    posts_map = map(validate_post, res.json())
    posts_list = list(posts_map)

    assert res.status_code == 200
    assert len(res.json()) == len(create_test_posts)

def test_get_all_posts_unauth(client, create_test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_get_post_unauth(client, create_test_posts):
    res = client.get(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 401

def test_get_post_auth_noexit(auth_client, create_test_posts):
    res = auth_client.get('/posts/100000000000')
    assert res.status_code == 404

def test_get_post_auth_exit(auth_client, create_test_posts):
    res = auth_client.get(f'/posts/{create_test_posts[0].id}')
    post = schema.PostVote(**res.json())
    assert res.status_code == 200
    assert post.Post.id == create_test_posts[0].id
    assert post.Post.content == create_test_posts[0].content
    assert post.Post.title == create_test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("new title2", "new content2", True),
    ("new title3", "new content3", True),

])
def test_create_post(auth_client, add_user, create_test_posts, title, content, published):
    res = auth_client.post('/posts/', json={"title":title, "content":content, "published":published})
    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == add_user['id']

def test_create_test_public_true(auth_client, add_user, create_test_posts):
    res = auth_client.post('/posts/', json={"title":"rafdafcac", "content":"dasdascs"})
    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "rafdafcac"
    assert created_post.content == "dasdascs"
    assert created_post.published == True
    assert created_post.owner_id == add_user['id']

def test_create_posts_unauth(client, add_user, create_test_posts):
    res = client.post('/posts/', json={"title":"rafdafcac", "content":"dasdascs"})
    assert res.status_code == 401

def test_delete_post_unauth(client, add_user, create_test_posts ):
    res = client.delete(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 401

def test_delete_post_auth(auth_client, add_user, create_test_posts ):
    res = auth_client.delete(f'/posts/{create_test_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_auth_noexit(auth_client, add_user, create_test_posts ):
    res = auth_client.delete('/posts/10000000000')
    assert res.status_code == 404

def test_delete_post_other_user_auth(auth_client, add_user, create_test_posts ):
    res = auth_client.delete(f'/posts/{create_test_posts[3].id}')
    assert res.status_code == 403

def test_update_post_auth(auth_client, add_user, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[0].id
    }
    res = auth_client.put(f'/posts/{create_test_posts[0].id}', json = data)
    updated_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.id == data["id"]
    assert updated_post.content == data["content"]
    assert updated_post.title == data["title"]

def test_update_post_other_user_auth(auth_client, add_user, add_user_2, create_test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[3].id
    }
    res = auth_client.put(f'/posts/{create_test_posts[3].id}', json = data)
    print (res.json())
    assert res.status_code == 403

def test_update_post_unauth(client, add_user, create_test_posts ):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[3].id
    }
    res = client.put(f'/posts/{create_test_posts[0].id}', json = data)
    assert res.status_code == 401

def test_update_post_auth_noexit(auth_client, add_user, create_test_posts ):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": create_test_posts[3].id
    }
    res = auth_client.put('/posts/10000000000', json = data)
    assert res.status_code == 404
