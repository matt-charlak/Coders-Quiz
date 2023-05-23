from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import UserProfile, Game, Quiz
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import random


def register(request):
    print("HI")
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile_url = '/user_profile/' + str(user_profile.id)
        return HttpResponseRedirect(user_profile_url)
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            bio = request.POST.get('bio', '')
            mobileNo = request.POST.get('mobileNo', '')
            gender = request.POST.get('gender', '')

            if User.objects.filter(username=username).exists():
                error = 'The Sap_id is already in use by another account.'
                return render(request, 'app/registration.html', {'error': error})

            else:
                user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                                last_name=last_name)
                user.set_password(password)
                user.save()
                Name = first_name + " " + last_name
                student = UserProfile.objects.create(user=user, Name=Name, bio=bio, mobileNo=mobileNo, gender=gender)
                student.save()
                auth_login(request, user)
                student_profile_url = '/user_profile/' + str(student.id)
                return HttpResponseRedirect(student_profile_url)
                # return render(request, 'user_profile/profile.html', {"student": student})
        else:
            return render(request, 'app/registration.html', {})


def login(request):
    print("HI")
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        student_profile_url = '/user_profile/' + str(user_profile.id)
        return HttpResponseRedirect(student_profile_url)
    else:
        print("IN")
        if request.method == 'POST':
            print("POST")
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                print('Inner IN')
                if user.is_active:
                    auth_login(request, user)
                    student_profile = UserProfile.objects.get(
                        user=request.user, )
                    student_profile_url = '/user_profile/' + str(student_profile.id)
                    return HttpResponseRedirect(student_profile_url)
                else:
                    error = 'Your account is disabled.'
                    return render(request, 'app/login.html', {'error': error})
            else:
                print('error')
                error = 'Incorrect Username or Password'
                return render(request, 'app/login.html', {'error': error})
        else:
            return render(request, 'app/login.html', {})


def logout(request):
    auth_logout(request)
    return redirect(reverse('app:login'))


@login_required(login_url='app:login')
def user_profile(request, id):
    client = get_object_or_404(UserProfile, id=id)
    user = UserProfile.objects.get(user=request.user)
    quiz = Quiz.objects.filter(user=user)
    return render(request, 'app/user_profile.html', {'client': client, 'req': request.user, 'quiz': quiz})


@login_required(login_url='app:login')
def search(request):
    user = request.user
    prof = UserProfile.objects.get(user=user)
    print(prof.id)
    questions = Game.objects.all()
    if request.GET.get('search'):
        param = request.GET.get('search')
        questions = Game.objects.filter(question__icontains=param)
        if not questions.exists():
            return render(request, 'app/search.html', {'error': 'NO MATCHING QUESTIONS FOUND', 'prof': prof})
        return render(request, 'app/search.html', {'questions': questions, 'prof': prof})
    return render(request, 'app/search.html', {'questions': questions, 'prof': prof})


@login_required(login_url='app:login')
def quiz(request):
    game = Game.objects.all()
    print(game)
    a = len(game)
    print(a)
    questions = []
    while(len(questions) != 4):
        k = random.randint(0, a-1)
        if questions.count(game[k]) == 0:
            questions.append(game[k])

    profile = UserProfile.objects.get(user=request.user)
    qu = Quiz.objects.create(user=profile, q1=questions[0], q2=questions[1], q3=questions[2], q4=questions[3])
    qu.save()
    print(qu)
    quiz_url = '/actualquiz/' + str(qu.id)
    return HttpResponseRedirect(quiz_url)


@login_required(login_url='app:login')
def actualquiz(request, id):
    if request.method == 'POST':
        count = 0
        s1 = request.POST.get('ques1', '')
        s2 = request.POST.get('ques2', '')
        s3 = request.POST.get('ques3', '')
        s4 = request.POST.get('ques4', '')
        quiz = Quiz.objects.get(id=id)
        if quiz.q1.answer == s1:
            count = count + 1
        if quiz.q2.answer == s2:
            count = count + 1
        if quiz.q3.answer == s3:
            count = count + 1
        if quiz.q4.answer == s4:
            count = count + 1
        quiz.q1selected = s1
        quiz.q2selected = s2
        quiz.q3selected = s3
        quiz.q4selected = s4
        quiz.save()
        user = request.user
        Profile = UserProfile.objects.get(user=user)
        Profile.totalQues = Profile.totalQues + 4
        Profile.totalAns = Profile.totalAns + count
        Profile.save()
        user_profile = UserProfile.objects.get(user=request.user)
        student_profile_url = '/user_profile/' + str(user_profile.id)
        return HttpResponseRedirect(student_profile_url)
    else:
        quiz = Quiz.objects.get(id=id)
        if not quiz.q1selected:
            game = Game.objects.all()
            a = len(game)
            options1 = [quiz.q1.answer]
            options2 = [quiz.q2.answer]
            options3 = [quiz.q3.answer]
            options4 = [quiz.q4.answer]
            while(len(options1) != 4):
                k = random.randint(0, a-1)
                if options1.count(game[k].answer) == 0:
                    options1.append(game[k].answer)

            while(len(options2) != 4):
                k = random.randint(0, a-1)
                if options2.count(game[k].answer) == 0:
                    options2.append(game[k].answer)

            while(len(options3) != 4):
                k = random.randint(0, a-1)
                if options3.count(game[k].answer) == 0:
                    options3.append(game[k].answer)

            while(len(options4) != 4):
                k = random.randint(0, a-1)
                if options4.count(game[k].answer) == 0:
                    options4.append(game[k].answer)
            options1.sort()
            options2.sort()
            options3.sort()
            options4.sort()
            print(options1)
            print(options2)
            print(options3)
            print(options4)
            return render(request, 'app/quiz.html', {'quiz': quiz, 'options1': options1, 'options2': options2,
                                                     'options3': options3, 'options4': options4, 'f': 0})
        else:
            quiz = Quiz.objects.get(id=id)
            return render(request, 'app/quiz.html', {'quiz': quiz, 'f': 1})
