from django.db import models
from django.contrib.auth.models import User




def path(instance, filename):
    """
    Generowanie wewnetrznej sciezki do przetrzymywania zdjec profilowych.
    np. : /MEDIA_ROOT/photos/abc.jpg

    :return: sciezka pliku ze zdjeciem profilowym
    """
    return 'photos/{0}'.format(filename)


class UserProfile(models.Model):
    """
    Wszystkie informacje na temat profilu uzytkownika korzystajacego z aplikacji.


    :user: nazwa uzytkownika
    :photo: zdjecie uzytkownika
    :Name: imie i nazwisko uzytkownika
    :bio: opis uzytkownika
    :gender: plec uzytkownika
    :mobileNo: telefon kontaktowy uzytkownika
    :totalQues: ilosc pytanie na ktore uzytkownika odpowiedzial
    :totalAns: ilosc pytan na ktore uzytkownika odpowiedzial poprawnie
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stud')
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
    """
    Ulubione kateogrie ktore uzytkownika wybral
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Game(models.Model):
    """
    Zbierane informacje ktore pozniej zostana wykorzystane do slownika synonimow oraz ich krotki opis

    :question: slowko do ktorego bedziemy szukac synonimu
    :answer: slownko ktore jest poprawna odpowiedzia do szukanego
    :description1: ktortki opis co dane slowko oznacza
    """
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=200, blank=True, null=True)
    description1 = models.CharField(max_length=200, blank=True, null=True)

    """
    :categorie: wybrana przez uzytkownika kategoria dane slowka
    """
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return str(self.question)


class Quiz(models.Model):
    """
    Model ktory zbiera informacje o pytaniu oraz odpowiedzi uzytkownika

    :q1 - q4: pytania ktore pytaja uzytkownika w momencie przeprowadzania quizu
    :q1selected - q4selected: odpowiedzi ktore zostaly wybrane przez uzytkownika
    """
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
    """
    Model zbierajacy wszystkie wyniki poprawnych odpoweidzi uzytkownikow w aplikacji (bazie danych)

    :totalAns: ilosc pytan na ktore uzytkownika odpowiedzial poprawnie
    :name: imie i nazwisko uzytkownika

    """
    totalAns = models.IntegerField()
    name = models.CharField(max_length=255)

    db_table = 'app_userprofile'