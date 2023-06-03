from django.db import models
from django.contrib.auth.models import User


# Generowanie wewnetrznej sciezki do przetrzymywania zdjec profilowych
# Np. : /MEDIA_ROOT/photos/abc.jpg

def path(instance, filename):
    return 'photos/{0}'.format(filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stud')

    # Zbieranie danych na temat profilu uzytkownika, podanych w formularzu
    # photo - zdjecie profilowe
    # name - nazwa uzytkownika
    # bio - opis uzytkownika
    # gender - plec uzykownika
    # mobileno - numer telefonu
    # totalquest - ilsoc pytania na ktore zostalo odpowiedziane
    # totalans - ilosc odpoweidzi ktore zostaly oddane
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


class Category(models.Model):
    # nazwy kateogrii gier
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Game(models.Model):

    #zbieranie danych na temat gry (slowek), ktorymi bedzie mozna dalej grac z innymi
    # question - slowko do zadania na ktore bedziemy odpowiadac
    # answer - slowno do zadania ktore bedzie odpowiedzia
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=200, blank=True, null=True)
    description1 = models.CharField(max_length=200, blank=True, null=True)

    # jedna kategoria ktora moze miec wiele gier
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return str(self.question)


class Quiz(models.Model):

    #przebieg generowania pytania oraz utrzymanie ciaglasci w zadanaich, brak powtarzania tego samego pytania
    #q1 nie bedzie takie samo jak q2 itd.

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    q1 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q1")
    q1selected = models.CharField(max_length=200, blank=True, null=True)
    q2 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q2")
    q2selected = models.CharField(max_length=200, blank=True, null=True)
    q3 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q3")
    q3selected = models.CharField(max_length=200, blank=True, null=True)
    q4 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="q4")
    q4selected = models.CharField(max_length=200, blank=True, null=True)


class UserProfileRanking(models.Model):

    #model ktory wyciaga z bazy caly ranking graczy ktorzy oddali odpowiedz w grze
    #ustawia ich w kolejnosc ilosci najwiecej odpowiedzi do najmniej

    totalAns = models.IntegerField()
    name = models.CharField(max_length=255)

    db_table = 'app_userprofile'