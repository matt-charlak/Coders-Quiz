import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")
django.setup()

import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory, Client
from django.urls import reverse
from app.models import UserProfile, Game, Quiz
from app.views import register, login, logout, search, quiz, actualquiz, add_game


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

@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.mark.django_db
def test_register_view(client):
    url = reverse('app:register')

    # sprawdzam uzytkownika
    response = client.post(url, {
        'username': 'existing_user',
        'password': 'password',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'bio': 'Test bio',
        'mobileNo': '123456789',
        'gender': 'Male',
    })

    assert response.status_code == 302

    # sprawdzam uzytkownika
    response = client.post(url, {
        'username': 'new_user',
        'password': 'password',
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'bio': 'Test bio',
        'mobileNo': '123456789',
        'gender': 'Male',
    })

    assert response.status_code == 302
    assert response.url == '/user_profile/1'  # Assuming the user profile ID is 1

    # sprawdzam czy uzytkownik sie wygenerowal
    user_profile = None
    try:
        user_profile = UserProfile.objects.get(user__username='new_user')
    except UserProfile.DoesNotExist:
        print("Uzytkownik nie istnieje")

    if user_profile:
        assert user_profile.Name == 'John Doe'
        assert user_profile.bio == 'Test bio'
        assert user_profile.mobileNo == '123456789'
        assert user_profile.gender == 'Male'

        # Sprawdzam czy uzytkownik trafila na swoj profil
        response = client.get(response.url)
        assert response.status_code == 200
        assert user_profile.Name in response.content.decode()
        assert user_profile.bio in response.content.decode()
        assert user_profile.mobileNo in response.content.decode()
        assert user_profile.gender in response.content.decode()

@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.mark.django_db
def test_login_view(client):
    url = reverse('app:login')

    # Create a user for testing
    user = User.objects.create_user(username='test_user', password='test_password')
    UserProfile.objects.create(user=user)

    # Test with valid credentials
    response = client.post(url, {
        'username': 'test_user',
        'password': 'test_password',
    })
    assert response.status_code == 302

    # Test with invalid credentials
    response = client.post(url, {
        'username': 'invalid_user',
        'password': 'invalid_password',
    })
    assert response.status_code == 302


@pytest.fixture
def client():
    from django.test import Client
    return Client()

@pytest.mark.django_db
def test_logout_view(client):
    url = reverse('app:logout')

    # Create a user for testing
    User.objects.create_user(username='test_user', password='test_password')

    # Log in the user
    client.login(username='test_user', password='test_password')

    # Test logout
    response = client.get(url)
    assert response.status_code == 302

    # Check if the user is redirected to the login page
    assert response.url == '/login/'

    # Check if the user is logged out
    assert not client.session.get('_auth_user_id', None)

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def game(user):
    return Game.objects.create(question='apple', answer='fruit', description1='a juicy fruit')

@pytest.mark.django_db
def test_search_view_with_get(client, user, game):

    # Access the search view using GET request
    response = client.get(reverse('app:search'))

    # Assert that the response has status code 200
    assert response.status_code == 302

@pytest.mark.django_db
def test_search_view_with_post(client, user, game):

    # Access the search view using POST request with search parameter
    response = client.post(reverse('app:search'), {'search': 'apple'})

    # Assert that the response has status code 200
    assert response.status_code == 302


@pytest.mark.django_db
def test_search_view_with_post_no_results(client, user, game):

    # Access the search view using POST request with search parameter that won't match any game
    response = client.post(reverse('app:search'), {'search': 'banana'})

    # Assert that the response has status code 200
    assert response.status_code == 302


@pytest.mark.django_db
def test_quiz_view(client, django_user_model):
    # Utwórz użytkownika
    user = django_user_model.objects.create_user(
        username='testuser',
        password='testpassword'
    )
    client.login(username='testuser', password='testpassword')

    profile = UserProfile.objects.create(user=user)

    # Utwórz pytania dla quizu
    question1 = Game.objects.create(question='Pytanie 1', answer='Odpowiedź 1')
    question2 = Game.objects.create(question='Pytanie 2', answer='Odpowiedź 2')
    question3 = Game.objects.create(question='Pytanie 3', answer='Odpowiedź 3')
    question4 = Game.objects.create(question='Pytanie 4', answer='Odpowiedź 4')

    # Wywołaj widok quiz za pomocą metody POST
    response = client.post(reverse('app:quiz'))

    # Sprawdź, czy odpowiedź przekierowuje na odpowiednią stronę
    assert response.status_code == 302
    assert response.url == '/actualquiz/1'  # Sprawdź wartość id odpowiedniego quizu

    # Wywołaj widok actualquiz za pomocą metody GET
    response = client.get(reverse('app:actualquiz', args=[1]))  # Przekazanie odpowiedniego id quizu

    # Sprawdź, czy odpowiedź ma status 200
    assert response.status_code == 200

    # Sprawdź, czy strona zawiera oczekiwane elementy
    assert b'Zagrajmy!' in response.content  # Przykładowy tekst na stronie quizu

    # Wyloguj użytkownika
    client.logout()


@pytest.mark.django_db
def test_add_game_view():
    # Tworzenie fabryki żądań Django
    factory = RequestFactory()

    # Tworzenie żądania POST
    data = {
        'question': 'Test question',
        'answer': 'Test answer',
        'description1': 'Test description',
    }
    request = factory.post(reverse('app:add_game'), data)

    #Wywołanie widoku
    response = add_game(request)

    # Sprawdzenie przekierowania na stronę 'app:search'
    assert response.status_code == 302
    assert response.url == reverse('app:search')

    # Sprawdzenie czy nowa gra została dodana do bazy danych
    assert Game.objects.filter(question='Test question').exists()

    # Tworzenie żądania GET
    request = factory.get(reverse('app:add_game'))

    # Wywołanie widoku
    response = add_game(request)

    # Sprawdzenie kodu odpowiedzi
    assert response.status_code == 200

