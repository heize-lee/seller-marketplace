from django import forms
from .models import Review


class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment','image','rating']
        labels = {
            'comment': '상세리뷰를 작성해주세요', 
        }
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control mt-2", "rows": 10}),
            'image': forms.ClearableFileInput(attrs={"class":"image-form"})
        }