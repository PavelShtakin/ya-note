import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_available(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200