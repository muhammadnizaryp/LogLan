from django.conf.urls import url
from . import views
from .forms import login_form
from django.contrib.auth.views import login

urlpatterns=[
        url(r'^$', views.home_view, name='home'),
        url(r'^sign-up/$', views.signup_view, name='signup'),
        url(r'^sign-up/succes/$', views.signup_succes_view, name='signup_succes'),
        url(r'^account/confirmation/(?P<activation_key>\w+)/$', views.account_confirmation_view, name='account_confirmation'),
        url(r'^account/confirmed/$', views.account_confirmed_view, name='account_confirmed'),
        url(r'^account/expired/$', views.account_expired_view, name='account_expired'),
        url(r'^login/$', login, name='login', kwargs={"authentication_form": login_form}),
        url(r'^help/$', views.help_view, name='help'),
        url(r'^ranking/$', views.ranking_view, name='ranking'),
        url(r'^logout/$', views.logout_view, name='logout'),
        url(r'^user-main-page/$', views.user_main_page_view, name='user_main_page'),
        url(r'^choose-level/$', views.choose_level_view, name='choose_level'),
        url(r'^course/(?P<course_slug>[\w-]+)/(?P<number_part_course>[0-9]+)/$', views.course_part_detail_view, name='course_part_detail'),
        url(r'^course/(?P<course_slug>[\w-]+)/part-list/$', views.course_part_list_view, name='course_part_list'),
        url(r'^course/(?P<course_slug>[\w-]+)/part-result/$', views.course_part_result_view, name='course_part_result'),
        url(r'^quiz/(?P<course_slug>[\w-]+)/(?P<number_part_quiz>[0-9]+)/$', views.quiz_part_detail_view, name='quiz_part_detail'),
        url(r'^quiz/(?P<course_slug>[\w-]+)/result/$', views.quiz_part_result_view, name='quiz_part_result'),
        url(r'^quiz/(?P<course_slug>[\w-]+)/retake/$', views.quiz_part_retake_view, name='quiz_part_retake'),
        url(r'^cek_jawaban/$', views.cek_jawaban, name='cek_jawaban'),
]
