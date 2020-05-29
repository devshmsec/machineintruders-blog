from django import forms
from allauth.account.forms import SignupForm
from .models import Comment


class RegisterForm(SignupForm):

    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name'}))

    field_order = [
        'first_name',
        'last_name',
        'email',
        'username',
        'password1',
        'password2'
    ]

    def save(self, request):

        user = super(RegisterForm, self).save(request)
        return user


class CommentForm(forms.ModelForm):

    attributes = {
        'rows': 2,
        'cols': 10,
        'placeholder': 'Comment here',
        'class': 'form-control'
    }

    text = forms.CharField(
        max_length=200, widget=forms.Textarea(attrs=attributes))

    class Meta:
        model = Comment
        fields = ('text',)
