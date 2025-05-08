import pytest
from django.test.client import Client
from notes.models import Note


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def note(author):
    return Note.objects.create(
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )


@pytest.fixture
def slug_for_args(note):
    return (note.slug,)


@pytest.fixture
def bulk_notes(author, not_author):
    notes = []
    for i in range(2):
        notes.append(Note.objects.create(
            title=f'Note {i} from Author',
            text='...',
            slug=f'author-{i}',
            author=author,
        ))
        notes.append(Note.objects.create(
            title=f'Note {i} from Not Author',
            text='...',
            slug=f'not-author-{i}',
            author=not_author,
        ))
    return notes