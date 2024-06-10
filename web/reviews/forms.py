from django import forms
from .models import Review

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment','image']
        labels = {
            'comment': '상세리뷰를 작성해주세요',
            'image' : '사진을 등록해주세요'
        }