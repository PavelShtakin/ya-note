import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture


@pytest.mark.parametrize(
    'name, method',
    (
        ('notes:home', 'get'),
        ('users:login', 'get'),
        ('users:signup', 'get'),
        ('users:logout', 'post'),
    )
)
def test_pages_availability_for_anonymous_user(client, name, method):
    url = reverse(name)
    response = getattr(client, method)(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:list', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    [
        (lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (lazy_fixture('author_client'), HTTPStatus.OK),
    ],
)
def test_pages_availability_for_different_users(
    parametrized_client, name, note, expected_status
):
    url = reverse(name, args=(note.slug,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    [
        ('notes:detail', lazy_fixture('slug_for_args')),
        ('notes:edit', lazy_fixture('slug_for_args')),
        ('notes:delete', lazy_fixture('slug_for_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ],
)
def test_redirects_for_anonymous_client(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
