from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': 'notfound@example.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    new_user = {
        "name": "Alice Johnson",
        "email": "alice@example.com"
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    # POST Ð²Ð¾Ð·Ð²Ñ€Ð°Ñ‰Ð°ÐµÑ‚ id Ñ�Ð¾Ð·Ð´Ð°Ð½Ð½Ð¾Ð³Ð¾ Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»Ñ�
    user_id = response.json()
    assert isinstance(user_id, int)
    get_response = client.get("/api/v1/user", params={'email': new_user["email"]})
    assert get_response.status_code == 200
    assert get_response.json()["email"] == new_user["email"]
    assert get_response.json()["name"] == new_user["name"]

def test_create_user_with_invalid_email():
    existing_email = users[0]["email"]
    duplicate_user = {
        "name": "Duplicate",
        "email": existing_email
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    email_to_delete = users[1]["email"]
    delete_response = client.delete("/api/v1/user", params={'email': email_to_delete})
    assert delete_response.status_code == 204
    assert delete_response.text == ""
    get_response = client.get("/api/v1/user", params={'email': email_to_delete})
    assert get_response.status_code == 404
