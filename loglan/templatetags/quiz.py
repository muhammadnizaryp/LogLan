from django import template
from ..models import Quiz, QuizTaken
register = template.Library()

@register.simple_tag
def user_quiz_point_per_level(user, quiz_id):
    point = 0
    quiz = Quiz.objects.get(id=quiz_id)
    quiz_taken, created = QuizTaken.objects.get_or_create(user=user, quiz=quiz)
    for quiz_part_is_true in quiz_taken.quiz_part_is_true.all():
        point += quiz_part_is_true.quiz_point
    return point
