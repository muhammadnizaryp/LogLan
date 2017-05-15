from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class UserProfileManager(models.Manager):
    def get_user_rangking(self):
        all_user = UserProfile.objects.all()
        return sorted(all_user, key=lambda user_profile:user_profile.user_point_total(), reverse=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    objects = models.Manager()
    user_profile_manager = UserProfileManager()

    def __str__(self):
        return self.user.username

    def user_course_point(self):
        point = 0
        course_taken_list = CourseTaken.objects.filter(user=self.user)
        for course_taken in course_taken_list:
            for course_part in course_taken.course_part.all():
                point += course_part.course_point
        return point

    def user_quiz_point(self):
        point = 0
        quiz_taken_list = QuizTaken.objects.filter(user=self.user)
        for quiz_taken in quiz_taken_list:
            for quiz_part_is_true in quiz_taken.quiz_part_is_true.all():
                point += quiz_part_is_true.quiz_point
        return point

    def user_point_total(self):
        point = 0
        user_point_total = self.user_course_point() + self.user_quiz_point()
        return user_point_total

    def user_ranking(self):
        rankings = list(UserProfile.user_profile_manager.get_user_rangking())
        return rankings.index(self) + 1


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
        ordering = ( 'course', 'number')

    def __str__(self):
        return '{} - [{}] {}'.format(self.course.course_name, self.number, self.course_part_name)

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

    def is_last_course_part(self):
        course_parts = CoursePart.objects.filter(course=self.course).reverse()
        if self == course_parts[0]:
            return True
        else:
            return False

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
            return None

class Quiz(models.Model):
    course = models.OneToOneField(Course, related_name='quiz')

    def __str__(self):
        return self.course.course_name

class QuizPartAnswer(models.Model):
    quiz_part = models.ForeignKey('QuizPart', related_name='quiz_part_answers', null=True)
    text_answer = models.TextField(blank=True, null=True)
    image_answer = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.text_answer, self.quiz_part.quiz_part_name)

class QuizPart(models.Model):
    number = models.IntegerField(null=True)
    quiz = models.ForeignKey(Quiz, related_name='quiz_parts')
    course_part = models.ForeignKey(CoursePart, related_name='quiz_parts_course')
    quiz_part_name = models.CharField(max_length=30)
    quiz_content = models.TextField()
    quiz_answer_key = models.ForeignKey(QuizPartAnswer, related_name='quiz_parts_answer_key', null=True, blank=True)
    quiz_point = models.IntegerField()

    class Meta:
        ordering = ( 'quiz', 'number')

    def __str__(self):
        return '[{}] {} - {}'.format(self.number, self.quiz_part_name, self.quiz.course.course_name)

    def next_quiz(self):
        quiz_part = QuizPart.objects.filter(quiz=self.quiz)
        try:
            next_quiz = quiz_part.filter(number__gt=self.number).order_by('number')[0]
            return next_quiz
        except IndexError:
            return None

    def previous_quiz(self):
        quiz_part = QuizPart.objects.filter(quiz=self.quiz)
        try:
            previous_quiz = quiz_part.filter(number__lt=self.number).order_by('-number')[0]
            return previous_quiz
        except IndexError:
            return None

    def is_last_quiz_part(self):
        quiz_parts = QuizPart.objects.filter(quiz=self.quiz).reverse()
        if self == quiz_parts[0]:
            return True
        else:
            return False

class QuizTaken(models.Model):
    user = models.ForeignKey(User, related_name='quiz_taken')
    quiz = models.ForeignKey(Quiz, related_name='quiz_takens')
    quiz_part_is_true = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_true',  blank=True)
    quiz_part_is_false = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_false',  blank=True)
    quiz_part_is_completed = models.ManyToManyField(QuizPart, related_name='quiz_takens_is_completed', blank=True)

    def __str__(self):
        return self.user.username

    def last_taken_quiz(self):
        quiz_parts_is_completed = self.quiz_part_is_completed.all()
        total = quiz_parts_is_completed.count()
        if quiz_parts_is_completed:
            if total>=1:
                return quiz_parts_is_completed[total-1]
        else:
            return None
