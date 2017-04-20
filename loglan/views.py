from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import hashlib, datetime, random
import hashlib
from .models import UserActivationKey, Course, CoursePart, QuizPart, CourseTaken
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

# Create your views here.
def home_view(request):
    return render(request, "loglan/home.html",)

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

def help_view(request):
    return render(request, "loglan/help.html")

def ranking_view(request):
    return render(request, "loglan/ranking.html")

def about_view(request):
    return render(request, "loglan/about.html")

def user_main_page_view(request):
    return render(request, "loglan/user_main_page.html")

def choose_level_view(request):
    context = {}
    courses = Course.objects.all()
    context['courses']=courses
    return render(request, "loglan/choose_level.html", context )

def course_part_detail_view(request, course_slug, id_part_course):
    course_part = CoursePart.objects.get(id=id_part_course)

    # cek udah pernah belajar course ini apa belom
    course_taken, created = CourseTaken.objects.get_or_create(
        user=request.user,
        course=course_part.course
    )

    # if created:
    #     pass
    # else:
    #     next_part = CoursePart.objects.filter(course=course_part.course).filter(id__gt=course_part.id).order_by('id')[0:1]
    #     # kalau udah pernah ngerjain, langsung diredirect ke part terakhir bener + next 1 part
    #
    #     return HttpResponseRedirect(reverse('course:course_part_detail', kwargs={'course_slug': course_part.course.course_slug, 'id_part_course': next_part_id}))
    #     pass
    context = {}
    context['course_part'] = course_part
    return render(request, "loglan/course_part_detail.html", context )

def course_part_list_view(request, course_slug):
    # show
    context = {}
    course = Course.objects.get(course_slug=course_slug)
    context['course'] = course
    return render(request, "loglan/course_part_list.html", context)

def quiz_part_detail_view(request,course_slug, id_part_quiz):
    context = {}
    quiz_part = QuizPart.objects.get(id=id_part_quiz)
    context['quiz_part'] = quiz_part
    return render(request,"loglan/quiz_part_detail.html", context)
