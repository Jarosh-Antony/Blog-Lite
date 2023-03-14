import pytest
from blog_app_lite import db
from GET_post import result_GET_Post

@pytest.mark.parametrize("login_credential,json_response",result_GET_Post())
def test_get(client, auth,login_credential,json_response):
    print('login_credential',login_credential)
    print('json_response',json_response)
    
    response = client.get('/post',headers=login_credential)

    
    assert json_response==response.json