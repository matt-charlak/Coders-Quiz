import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")
django.setup()

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory, Client
from django.urls import reverse
from app.models import UserProfile, Game, Quiz
from app.views import register, login, logout, search, quiz, actualquiz


@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def logged_in_user(request_factory):
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    request = request_factory.post(reverse('register'))
    request.user = user

    return request

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def authenticated_request(request_factory):
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    request = request_factory.post(reverse('app:register'), data={
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'bio': 'Some bio',
        'mobileNo': '123456789',
        'gender': 'Male'
    })
    request.user = user
    return request

@pytest.mark.django_db
def test_register_create_new_user(authenticated_request):
    response = register(authenticated_request)
    assert response.status_code == 302

def test_register_url_resolves():
    url = reverse('app:register')
    assert url == '/register/'

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def authenticated_request(request_factory):
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    request = request_factory.post(reverse('app:login'), data={
        'username': 'testuser',
        'password': 'testpassword',
    })

    request.user = user
    return request

@pytest.fixture
def unauthenticated_request(request_factory):
    return request_factory.get(reverse('app:login'))

@pytest.mark.django_db
def test_login_authenticated(authenticated_request):
    response = login(authenticated_request)
    assert response.status_code == 302

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def authenticated_client(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    client = Client()
    client.force_login(user)
    return client

@pytest.fixture
def unauthenticated_client(client):
    return client

@pytest.mark.django_db
def test_logout(authenticated_client):
    response = authenticated_client.get(reverse('app:logout'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_search(authenticated_client):
    response = authenticated_client.get(reverse('app:search'))
    assert response.status_code == 200

    # Przykładowa asercja sprawdzająca obecność danych w kontekście renderowanego widoku
    assert 'questions' in response.context
    questions = list(response.context['questions'])
    assert isinstance(questions, list)

    assert 'prof' in response.context
    prof = response.context['prof']
    assert isinstance(prof, UserProfile)

@pytest.fixture
def authenticated_request(request_factory):
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    request = request_factory.get(reverse('app:quiz'))
    request.user = user
    return request

@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    return user

@pytest.mark.django_db
def test_quiz(authenticated_user, client):
    # Uwierzytelnienie klienta testowego
    client.force_login(authenticated_user)

    # Tworzenie danych testowych
    questions = []
    for i in range(4):
        questions.append(Game.objects.create(question=f'Question {i}'))

    # Wykonanie żądania HTTP
    response = client.get(reverse('app:quiz'))

    # Sprawdzenie odpowiedzi
    assert response.status_code == 302

    # Sprawdzenie przekierowania na stronę quizu
    quiz_obj = Quiz.objects.first()
    assert response.url == reverse('app:actualquiz', args=[quiz_obj.id])

    # Sprawdzenie utworzonego obiektu Quiz
    assert quiz_obj.q1 in questions
    assert quiz_obj.q2 in questions
    assert quiz_obj.q3 in questions
    assert quiz_obj.q4 in questions


@pytest.mark.django_db
def test_add_game(authenticated_user, client):
    # Uwierzytelnienie klienta testowego
    client.force_login(authenticated_user)

    # Wykonanie żądania HTTP
    response = client.get(reverse('app:add_game'))

    # Sprawdzenie odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie formularza w odpowiedzi
    assert 'form' in response.context

    # Przesłanie formularza
    response = client.post(
        reverse('app:add_game'),
        {'question': 'Test Question', 'answer': 'Test Answer'}
    )

    # Sprawdzenie przekierowania po dodaniu słówka
    assert response.status_code == 302
    assert response.url == reverse('app:search')

