from django import forms
from operator_manager.models.operator import Operator
from user_manager.models.user import User
from django.core.validators import *
from reviews.models.review import Review





TYPE_CHOICES = [
    (1, '★1'),
    (2, '★2'),
    (3, '★3'),
    (4, '★4'),
    (5, '★5'),
]

#レビューフォーム
class ReviewForm(forms.Form):
    grade = forms.ChoiceField(label='評価', required=True, choices=TYPE_CHOICES)
    comment = forms.CharField(label='コメント', required=True, max_length=200, widget=forms.Textarea())
