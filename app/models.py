from django.db import models
from django.contrib.auth.models import User


# Creating a custom path for storing the user photos
# Example : /MEDIA_ROOT/photos/abc.jpg
def path(instance, filename):
    return 'photos/{0}'.format(filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stud')

    # username password fname lname email
    photo = models.FileField(blank=True, null=True, upload_to=path)
    Name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    mobileNo = models.CharField(max_length=50, blank=True, null=True)
    totalQues = models.IntegerField(blank=True, null=True, default=0)
    totalAns = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.Name)


class Game(models.Model):
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=200, blank=True, null=True)
    description1 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.question)


class Quiz(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    q1 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q1")
    q1selected = models.CharField(max_length=200, blank=True, null=True)
    q2 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q2")
    q2selected = models.CharField(max_length=200, blank=True, null=True)
    q3 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q3")
    q3selected = models.CharField(max_length=200, blank=True, null=True)
    q4 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q4")
    q4selected = models.CharField(max_length=200, blank=True, null=True)

