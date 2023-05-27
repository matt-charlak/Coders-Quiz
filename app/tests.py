from django.test import TestCase
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