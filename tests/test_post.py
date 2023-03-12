import pytest
from blog_app_lite import db


def test_get(client, auth):
    response = client.get('/post')
    assert response.status=='302 FOUND'
    assert b"login" in response.data

    auth_response=auth.login(username="lince",password="12345678")
    assert auth_response.status=='200 OK'
    
    response = client.get('/post',
                            headers={
                                'Authorization':auth_response.json['response']['user']['authentication_token']
                            })

    
    assert 'posts' in response.json
    posts=response.json['posts']
    
    assert len(posts)==3
    assert posts[0]['id']==6
    assert posts[0]['title']=='post1'
    assert posts[0]['description']=='this is my post 1 by jarosh'
    assert posts[0]['timestamp']=='2023-03-08 13:09:03.858694'
    assert posts[0]['imageurl']=='..\\post_images\\1_2023-03-08-13-09-03-858694_Snapshot_245.png'
    
    assert posts[1]['id']==7
    assert posts[1]['title']=='post2'
    assert posts[1]['description']=='this is my post 2 by jarosh'
    assert posts[1]['timestamp']=='2023-03-08 13:09:40.227679'
    assert posts[1]['imageurl']=='..\\post_images\\1_2023-03-08-13-09-40-227679_Snapshot_241.png'
    
    assert posts[2]['id']==8
    assert posts[2]['title']=='post1'
    assert posts[2]['description']=='this is my post 1 by thomas'
    assert posts[2]['timestamp']=='2023-03-08 13:10:46.917875'
    assert posts[2]['imageurl']=='..\\post_images\\2_2023-03-08-13-10-46-917875_Snapshot_243.png'