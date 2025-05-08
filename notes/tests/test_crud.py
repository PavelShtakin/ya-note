import pytest

from http import HTTPStatus
from django.urls import reverse

from notes.models import Note


@pytest.mark.django_db
def test_author_can_create_note(author_client, django_user_model):
    url = reverse('notes:add')
    form_data = {
        'title': 'Новая заметка',
        'text': 'Содержимое',
        'slug': 'new-note',
    }
    response = author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.FOUND
    assert Note.objects.filter(slug='new-note').exists()
    note = Note.objects.get(slug='new-note')
    assert note.author.username == 'Автор'


@pytest.mark.django_db
def test_author_can_edit_own_note(author_client, note):
    url = reverse('notes:edit', args=(note.slug,))
    updated_data = {
        'title': 'Обновлённый заголовок',
        'text': 'Обновлённый текст',
        'slug': note.slug,
    }
    response = author_client.post(url, data=updated_data)
    assert response.status_code == HTTPStatus.FOUND
    note.refresh_from_db()
    assert note.title == 'Обновлённый заголовок'
    assert note.text == 'Обновлённый текст'


@pytest.mark.django_db
def test_author_can_delete_note(author_client, note):
    url = reverse('notes:delete', args=(note.slug,))
    response = author_client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert not Note.objects.filter(slug=note.slug).exists()


@pytest.mark.django_db
def test_slug_must_be_unique(author_client, note):
    url = reverse('notes:add')
    form_data = {
        'title': 'Другая заметка',
        'text': 'Другое содержимое',
        'slug': note.slug
    }
    response = author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.OK
    form = response.context['form']
    assert 'slug' in form.errors


@pytest.mark.django_db
def test_not_author_cannot_edit_note(not_author_client, note):
    url = reverse('notes:edit', args=(note.slug,))
    response = not_author_client.post(url, data={
        'title': 'Попытка взлома',
        'text': 'Я не автор',
        'slug': note.slug
    })
    assert response.status_code == HTTPStatus.NOT_FOUND
    note.refresh_from_db()
    assert note.title != 'Попытка взлома'


@pytest.mark.django_db
def test_not_author_cannot_delete_note(not_author_client, note):
    url = reverse('notes:delete', args=(note.slug,))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Note.objects.filter(slug=note.slug).exists()

