from django import forms

from users.models import UserMovie

class ReviewForm(forms.ModelForm):
    review = forms.CharField(required=False)
    mark = forms.CharField(required=False)
    
    class Meta:
        model = UserMovie
        fields = ['review', 'mark']