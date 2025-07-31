import pytest 
from rest_framework.test import APIClient

# authentication function
def authenticate(client):
    register_payload = {
        "email": "restaurantadmin10@example.com",
        "password": "123",
        "user_type": "restaurant_admin"
    }

    client.post("/api/v1/register/", register_payload)

    login_payload = {
        "email": "restaurantadmin10@example.com",
        "password": "123" 
    }

    login_response = client.post("/api/v1/login/", login_payload)
    access_token = login_response.data["access"]
    return access_token


# creating a restaurant tests
@pytest.mark.django_db
def test_create_restaurant_success():
    client = APIClient()
    access_token = authenticate(client)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    restaurant_payload = {
        "name" : "Test Restaurant",
        "location" : "Saket",
        "opening_time" : "",
        "closing_time" : ""

    }

    response = client.post("/api/v1/restaurants/",restaurant_payload )

    assert response.status_code == 201
    assert "message" in response.data
    assert restaurant_payload["name"] in response.data["message"]

@pytest.mark.django_db
def test_create_restaurant_failure():
    client = APIClient()
    access_token = authenticate(client)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")


    restaurant1_payload = {
        "name" : "Test Restaurant",
        "location" : "Saket",
        "opening_time" : "",
        "closing_time" : ""

    }

    client.post("/api/v1/restaurants/",restaurant1_payload )

    restaurant2_payload = {
        # Dublicate restaurant with different timmings
        "name" : "Test Restaurant",
        "location" : "Saket",
        "opening_time" : "10:00:00",
        "closing_time" : "19:00:00"
    }

    response = client.post("/api/v1/restaurants/", restaurant2_payload)

    assert response.status_code == 400



# getting a restaurant tests

@pytest.mark.django_db
def test_get_restaurant_success():
    client = APIClient()
    access_token = authenticate(client)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    restaurant_payload = [{
        "name" : "Test Restaurant",
        "location" : "Saket",
        "opening_time" : "",
        "closing_time" : ""
    },
    {
        "name" : "Test Restaurant 2",
        "location" : "Saket",
        "opening_time" : "",
        "closing_time" : ""
    }]
    
    for restaurant in restaurant_payload:
        client.post("/api/v1/restaurants/", restaurant)

    
    
    response = client.get("/api/v1/restaurants/")

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Test Restaurant"
    assert response.data[1]["name"] == "Test Restaurant 2"
    assert isinstance(response.data, list)


# changing something in restaurant tests

from django.urls import reverse
from api.models import Restaurant, User

@pytest.mark.django_db
def test_put_restaurant_success():
    client = APIClient()

    owner1 = User.objects.create_user(email='owner1@gmail.com', password='123', user_type='restaurant_admin')
    owner2 = User.objects.create_user(email='owner2@gmail.com', password='123', user_type='restaurant_admin')

    r1 = Restaurant.objects.create(name='Dominos', location='Assam', opening_time=None, closing_time=None, owner=owner1)
    r2 = Restaurant.objects.create(name='ominos', location='Assam', opening_time=None, closing_time=None, owner=owner2)
    r3 = Restaurant.objects.create(name='minos', location='Assam', opening_time=None, closing_time=None, owner=owner1)

    response_register = client.post('/api/v1/login/', data={'email':'owner1@gmail.com', 'password':'123'})
    access_token = response_register.data['access']

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    url = f'/api/v1/restaurants/{r1.id}/'
    payload = {
        'name': 'Dominos',
        'location' : 'Delhi'
    }   

    response = client.put(url, data=payload)
    assert response.status_code == 200
    assert response.data['data']['location'] == 'Delhi'
    assert response.data['data']['name'] == 'Dominos'

@pytest.mark.django_db
def test_get_delete_restaurant_by_id():
    client = APIClient()
    access_token = authenticate(client)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    payload_restaurant = {
        "name" : "Dominos",
        "location" : "mumbai",
        
    }

    client.post('/api/v1/restaurants/', payload_restaurant)

    r_id = Restaurant.objects.first().id

    response = client.get(f'/api/v1/restaurants/{r_id}/')

    assert response.status_code == 200
    assert response.data['name'] == 'Dominos'
    assert response.data['opening_time'] == None 

    response = client.delete(f'/api/v1/restaurants/{r_id}/')

    assert response.status_code == 204

    response = client.get(f'/api/v1/restaurants/{r_id}/')

    assert response.status_code == 404

    



    

    













