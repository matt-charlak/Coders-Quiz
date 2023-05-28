from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Game, Quiz

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, Name='Kon Zwalony')
        self.game = Game.objects.create(question='Question 1', answer='Answer 1')

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.Name, 'Kon Zwalony')

    def test_game_creation(self):
        self.assertEqual(self.game.question, 'Question 1')
        self.assertEqual(self.game.answer, 'Answer 1')

    def test_quiz_creation(self):
        quiz = Quiz.objects.create(user=self.user_profile, q1=self.game, q2=self.game, q3=self.game, q4=self.game)
        self.assertEqual(quiz.user, self.user_profile)
        self.assertEqual(quiz.q1, self.game)
        self.assertEqual(quiz.q2, self.game)
        self.assertEqual(quiz.q3, self.game)
        self.assertEqual(quiz.q4, self.game)

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')        # Create UserProfile
        self.user_profile = UserProfile.objects.create(user=self.user, Name='Test User')        # Create some games for testing
        self.game1 = Game.objects.create(question='Question 1', answer='Answer 1')
        self.game2 = Game.objects.create(question='Question 2', answer='Answer 2')
        self.game3 = Game.objects.create(question='Question 3', answer='Answer 3')

    def test_register_view_authenticated_user(self):
        # Test register view with an authenticated user
        self.client.force_login(self.user)
        response = self.client.get(reverse('app:register'))
        self.assertRedirects(response, '/user_profile/1')

    def test_register_view_post_request(self):
        # Test register view with a POST request
        response = self.client.post(reverse('app:register'), {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'bio': 'Bio',
            'mobileNo': '1234567890',
            'gender': 'Male'
        })
        self.assertRedirects(response, '/user_profile/2')
        # Assert that a new user and UserProfile were created
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(UserProfile.objects.count(), 2)
        # Assert that the created user has the correct attributes
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'User')
        # Assert that the UserProfile was created correctly
        new_user_profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(new_user_profile.Name, 'New User')
        self.assertEqual(new_user_profile.bio, 'Bio')
        self.assertEqual(new_user_profile.mobileNo, '1234567890')
        self.assertEqual(new_user_profile.gender, 'Male')
        # Write similar test methods for other views...

    def test_add_game_view_post_request(self):
        # Test add_game view with a POST request
        self.client.force_login(self.user)
        response = self.client.post(reverse('app:add_game'), {
            'question': 'New Question',
            'answer': 'New Answer'
        })
        # Assert that a new game was created
        self.assertEqual(Game.objects.count(), 4)
        new_game = Game.objects.last()
        self.assertEqual(new_game.question, 'New Question')
        self.assertEqual(new_game.answer, 'New Answer')