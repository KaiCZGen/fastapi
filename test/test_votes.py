import pytest
from app import models

@pytest.fixture
def creat_votes(create_test_posts, session, add_user):
    new_vote = models.Votes(user_id=add_user['id'], post_id= create_test_posts[3].id)
    session.add(new_vote)
    session.commit()

def test_vote_on_post(auth_client, create_test_posts):
    res = auth_client.post("/votes/", json = {"post_id": create_test_posts[3].id, "post_dir":1})
    assert res.status_code == 201

def test_vote_on_post_twice(auth_client, create_test_posts, creat_votes):
    res = auth_client.post("/votes/", json = {"post_id": create_test_posts[3].id, "post_dir":1})
    assert res.status_code == 409

def test_delete_vote(auth_client, create_test_posts, creat_votes):
    res = auth_client.post("/votes/", json = {"post_id": create_test_posts[3].id, "post_dir":0})
    assert res.status_code == 201

def test_delete_vote_noexit(auth_client, create_test_posts):
    res = auth_client.post("/votes/", json = {"post_id": create_test_posts[3].id, "post_dir":0})
    assert res.status_code == 404

def test_add_vote_noexit(auth_client, create_test_posts):
    res = auth_client.post("/votes/", json = {"post_id": 100000000, "post_dir":0})
    assert res.status_code == 404

def test_add_vote_unauth(client, create_test_posts):
    res = client.post("/votes/", json = {"post_id": create_test_posts[3].id, "post_dir":0})
    assert res.status_code == 401
