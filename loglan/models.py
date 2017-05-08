from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")

    def __str__(self):
        return self.user.username

    def user_course_point(self):
        point = 0
        course_taken_list = CourseTaken.objects.filter(user=self.user)
        for course_taken in course_taken_list:
            for course_part in course_taken.course_part.all():
                point += course_part.course_point
        return point

class UserActivationKey(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_description = models.TextField()
    course_slug = models.SlugField(max_length=50, null=True)

    def __str__(self):
        return self.course_name

class CoursePart(models.Model):
    number = models.IntegerField(null=True)
    course = models.ForeignKey(Course, related_name='course_parts')
    course_part_name = models.CharField(max_length=50)
    course_content = models.TextField()
    course_example = models.TextField()
    course_example_answer_key = models.TextField()
    course_point = models.IntegerField()

    class Meta:
        ordering = ('number', )

    def __str__(self):
        return self.course_part_name

    def next_part(self):
        course_parts = CoursePart.objects.filter(course=self.course)
        try:
            next_part = course_parts.filter(number__gt=self.number).order_by('number')[0]
            return next_part
        except IndexError:
            return None

    def previous_part(self):
        course_parts = CoursePart.objects.filter(course=self.course)
        try:
            next_part = course_parts.filter(number__lt=self.number).order_by('-number')[0]
            return next_part
        except IndexError:
            return None

class CourseTaken(models.Model):
    user = models.ForeignKey(User, related_name='course_takens_user')
    course = models.ForeignKey(Course, related_name='course_takens')
    course_part = models.ManyToManyField(CoursePart, blank=True, related_name='course_takens_part')
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def last_taken_part(self):
        course_parts = self.course_part.all()
        total = course_parts.count()
        if course_parts:
            if total>=1:
                # ambil part yang terakhir dikerjain
                return course_parts[total-1]
        else:
            course_parts[0]

class Quiz(models.Model):
    course = models.OneToOneField(Course, related_name='quiz')

    def __str__(self):
        return self.course.course_name

class QuizPartAnswer(models.Model):
    quiz_part = models.ForeignKey('QuizPart', related_name='quiz_part_answers', null=True)
    text_answer = models.TextField(blank=True, null=True)
    image_answer = models.ImageField(blank=True, null=True)

    def __str__(self):
         return self.text_answer

class QuizPart(models.Model):
    number = models.IntegerField(null=True)
    quiz = models.ForeignKey(Quiz, related_name='quiz_parts')
    course_part = models.ForeignKey(CoursePart, related_name='quiz_parts_course')
    quiz_part_name = models.CharField(max_length=30)
    quiz_content = models.TextField()
    quiz_answer_key = models.ForeignKey(QuizPartAnswer, related_name='quiz_parts_answer_key')
    quiz_point = models.IntegerField()

    def __str__(self):
        return self.quiz_part_name

    def next_quiz(self):
        quiz_part = QuizPart.objects.filter(quiz=self.quiz)
        try:
            next_quiz = quiz_part.filter(number__gt=self.number).order_by('number')[0]
            return next_quiz
        except IndexError:
            return None

class QuizTaken(models.Model):
    user = models.OneToOneField(User, related_name='quiz_taken')
    quiz = models.ForeignKey(Quiz, related_name='quiz_takens')
    quiz_part_is_true = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_true')
    quiz_part_is_false = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_false')
    quiz_part_is_completed = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_completed')

    def __str__(self):
        return self.user.username
