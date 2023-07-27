from app import schema
from jose import jwt
from app.config import settings
import pytest

'''def test_root(client):
    res = client.get("/")
    assert (res.json().get('Message')) == 'Welcome to my FastAPI!!!'
    assert (res.status_code) == 200'''

def test_create_user(client):
    res = client.post("/users/", json={"email":"example@gmail.com", "password": "123"})
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "example@gmail.com"
    assert res.status_code == 201

def test_login_user(add_user, client):
    # session -> cleint -> add_user
    res = client.post("/login", data={"username":add_user['email'], "password": add_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.token_pwd, algorithms=[settings.algorithm])
    id: int = payload.get("user_id")
    assert res.status_code == 200
    assert login_res.token_type == 'bearer'
    assert id == add_user['id']

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '123', 403),
    ('example@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, '123', 422),
    ('example@gmail.com', None, 422)
])
def test_login_fail(add_user, client, email, password, status_code):
    res = client.post("/login", data={"username":email, "password": password})
    
    assert res.status_code == status_code
