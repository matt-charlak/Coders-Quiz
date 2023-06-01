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

    def test_user_profile_str_representation(self):
        self.assertEqual(str(self.user_profile), 'Kon Zwalony')

    def test_game_str_representation(self):
        self.assertEqual(str(self.game), 'Question 1')

    def test_user_profile_update_name(self):
        self.user_profile.Name = 'New Name'
        self.user_profile.save()
        updated_user_profile = UserProfile.objects.get(id=self.user_profile.id)
        self.assertEqual(updated_user_profile.Name, 'New Name')

    def test_game_update_question(self):
        self.game.question = 'Updated Question'
        self.game.save()
        updated_game = Game.objects.get(id=self.game.id)
        self.assertEqual(updated_game.question, 'Updated Question')

    def test_quiz_update_question(self):
        quiz = Quiz.objects.create(user=self.user_profile, q1=self.game, q2=self.game, q3=self.game, q4=self.game)
        quiz.q1 = Game.objects.create(question='Updated Question', answer='Updated Answer')
        quiz.save()
        updated_quiz = Quiz.objects.get(id=quiz.id)
        self.assertEqual(updated_quiz.q1.question, 'Updated Question')
        self.assertEqual(updated_quiz.q1.answer, 'Updated Answer')

