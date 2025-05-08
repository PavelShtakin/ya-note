import pytest
from django.urls import reverse
from http import HTTPStatus

@pytest.mark.django_db
def test_user_sees_only_own_notes(author_client, author, bulk_notes):
    url = reverse('notes:list')
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK
    notes = response.context['object_list']
    assert all(note.author == author for note in notes)
    assert len(notes) == 2