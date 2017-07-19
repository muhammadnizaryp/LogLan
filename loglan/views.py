from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import hashlib, datetime, random
import hashlib
import json
from .models import UserActivationKey, Course, CoursePart, QuizPart, CourseTaken, QuizTaken, QuizPartAnswer, UserProfile
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

# Create your views here.
def home_view(request):
    return render(request, "loglan/home.html")

def about_view(request):
    return render(request, "loglan/about.html")

def help_view(request):
    return render(request, "loglan/help.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            activation_key = hashlib.sha224((email).encode('utf-16be')).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user=User.objects.get(username=username)
            user_activation_key = UserActivationKey(user=user, activation_key=activation_key, key_expires=key_expires)
            user_activation_key.save()

            user_profile = UserProfile(user=user)
            user_profile.save()

            host=request.META['HTTP_HOST']
            email_subject = 'Account confirmation'
            email_body = "Hallo {}, Thanks for signing up. Wellcome to LogLan, web application e-learning platform to learn Python programming language,\
             this e-learning is deployed for research purpose. For activation your account, please click on the link below in less than 48 hours. \
             http://{}/account/confirmation/{}".format(username, host, activation_key)

            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email, settings.EMAIL_HOST_USER]

            send_mail(email_subject, email_body, from_email, to_email, fail_silently=False)

            return HttpResponseRedirect('/sign-up/succes')

    else:
        form = SignupForm()

    return render(request, 'loglan/signup.html', {'form': form})

def account_confirmation_view(request, activation_key):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user_main_page.html')

    user_activation = get_object_or_404(UserActivationKey, activation_key=activation_key)
    if user_activation.key_expires < timezone.now():
        return render_to_response('/account_expired.html')
    user = user_activation.user
    user.is_active = True
    user.save()
    return render_to_response('loglan/account_confirmed.html')

def account_confirmed_view():
    return render(request, "loglan/account_confirmed.html")

def account_expired_view():
    return render(request, "loglan/account_expired.html")

def signup_succes_view(request):
    return render(request, "loglan/signup_succes.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')

def ranking_view(request):
    context = {}
    user_profiles = UserProfile.objects.all()
    user_rankings = UserProfile.user_profile_manager.get_user_rangking()
    context['user_rankings'] = user_rankings
    return render(request, "loglan/ranking.html", context)

def user_main_page_view(request):
    context = {}
    course_taken = CourseTaken.objects.filter(user=request.user)
    context['course_taken']=course_taken
    return render(request, "loglan/user_main_page.html", context)


def choose_level_view(request):
    context = {}
    courses = Course.objects.all()
    context['courses']=courses
    return render(request, "loglan/choose_level.html", context )


def quiz_part_detail_view(request, course_slug, number_part_quiz):
    quiz_part = QuizPart.objects.get(number=number_part_quiz, quiz__course__course_slug = course_slug)

    quiz_taken, created = QuizTaken.objects.get_or_create(
        user=request.user,
        quiz=quiz_part.quiz
    )
    try:
        if number_part_quiz != '1' and (quiz_part.previous_quiz() != quiz_taken.last_taken_quiz()):
            if quiz_taken.last_taken_quiz():
                return HttpResponseRedirect('/quiz/{}/{}/'.format(course_slug, quiz_taken.last_taken_quiz().next_quiz().number))
            else:
                return HttpResponseRedirect('/quiz/{}/{}/'.format(course_slug, 1))
        else:
            if quiz_part in quiz_taken.quiz_part_is_completed.all():
                return HttpResponseRedirect('/quiz/{}/{}/'.format(course_slug, quiz_taken.last_taken_quiz().next_quiz().number))
    except:
        return HttpResponseRedirect('/quiz/{}/result'.format(course_slug))


    # kalau nomor quiz 1, quiz_part_is_true sama false harus dikosongin
    # if number_part_quiz == 1:

    if request.method == "POST":
        jawaban_id = int(request.POST.get("ChoiceAnswer"))
        jawaban = QuizPartAnswer.objects.get(id=jawaban_id)
        print(jawaban_id)
        if quiz_part.quiz_answer_key.id == jawaban_id:
            quiz_taken.quiz_part_is_true.add(quiz_part)
            pass
        else:
            pass
            quiz_taken.quiz_part_is_false.add(quiz_part)
        quiz_taken.quiz_part_is_completed.add(quiz_part)
        if quiz_part.is_last_quiz_part():
            return HttpResponseRedirect('/quiz/{}/result'.format(course_slug))
        else:
            return HttpResponseRedirect('/quiz/{}/{}/'.format(course_slug, quiz_part.next_quiz().number))

    context = {}
    context['quiz_part'] = quiz_part
    return render(request, "loglan/quiz_part_detail.html", context)

def quiz_part_result_view(request, course_slug):
    quiz_taken, created = QuizTaken.objects.get_or_create(
        user=request.user,
        quiz__course__course_slug=course_slug
    )
    context = {'quiz_taken': quiz_taken}
    return render(request, "loglan/quiz_part_result.html", context )

def quiz_part_retake_view(request, course_slug):
    # context = {}
    # context [''] =
    quiz_taken, created = QuizTaken.objects.get_or_create(
        user=request.user,
        quiz__course__course_slug=course_slug
    )
    quiz_taken.quiz_part_is_true.clear()
    quiz_taken.quiz_part_is_false.clear()
    quiz_taken.quiz_part_is_completed.clear()

    return HttpResponseRedirect('/quiz/{}/{}/'.format(course_slug, 1))


def course_part_detail_view(request, course_slug, number_part_course):
    course = Course.objects.get(course_slug=course_slug)
    course_part = CoursePart.objects.get(number=number_part_course, course=course)

    # cek udah pernah belajar course ini apa belom
    course_taken, created = CourseTaken.objects.get_or_create(
        user=request.user,
        course=course_part.course
    )

    if number_part_course != '1' and (course_part.previous_part() not in course_taken.course_part.all()):
        if course_taken.last_taken_part():
            return HttpResponseRedirect('/course/{}/{}/'.format(course_slug, course_taken.last_taken_part().next_part().number))
        else:
            return HttpResponseRedirect('/course/{}/{}/'.format(course_slug, 1))

    context = {}
    context['course_part'] = course_part
    return render(request, "loglan/course_part_detail.html", context )

def course_part_list_view(request, course_slug):
    context = {}
    course = Course.objects.get(course_slug=course_slug)
    # cek udah pernah belajar course ini apa belom
    course_taken, created = CourseTaken.objects.get_or_create(
        user=request.user,
        course=course
    )

    if created:
        course_taken.course_part.add(course.course_parts.all()[0])

    context['course'] = course
    context['course_taken'] = course_taken
    return render(request, "loglan/course_part_list.html", context)

def course_part_result_view(request, course_slug):
    context = {}
    course = Course.objects.get(course_slug=course_slug)
    context['course'] = course
    return render(request, "loglan/course_part_result.html", context)

def cek_jawaban(request):
    if request.method == 'POST':
        kode_jawaban = request.POST.get('jawaban')
        console_user = request.POST.get('console_user')
        user_id = request.POST.get('user_id')
        course_part_id = request.POST.get('course_part_id')
        response_data = {}
        user = User.objects.get(id=int(user_id))
        soal = CoursePart.objects.get(id=int(course_part_id))

        print('soal.id', soal.id)
        print('soal.course_example_answer_key: ', soal.course_example_answer_key)
        kunci = soal.course_example_answer_key.replace(u'\r',u'')
        kunci =u'{}\n'.format(kunci)

        print('kode_jawaban: ', kode_jawaban)
        print('kunci: ', kunci)
        if kunci == kode_jawaban:
            hasil_jawaban = "Kode program Anda benar"
            course_taken = CourseTaken.objects.get(user=request.user, course=soal.course)
            course_taken.course_part.add(soal)
            if soal.is_last_course_part():
                course_taken.is_done = True
            course_taken.save()

        else:
            hasil_jawaban = "Kode program Anda salah"

        response_data['hasil_jawaban'] = hasil_jawaban
        response_data['jawaban_html'] = kode_jawaban
        print(response_data)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")
