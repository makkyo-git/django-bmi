from django import forms
from django.contrib.auth.forms import( AuthenticationForm )
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

"アカウント登録フォーム"
class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'password1', 'password2',
        )
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

"アカウント更新フォーム"
class AccountsUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [ 
        ('男性', '男性'),
        ('女性', '女性'),
        ('その他', 'その他'),
    ]
    gender = forms.ChoiceField(label='性別', choices=GENDER_CHOICES)
    birthdate = forms.DateField(label='生年月日', widget=forms.DateInput(attrs={'type': 'date'}),)

    class Meta:
        model = User
        fields = (
            'icon',
            'username', 'email',
            'birthdate', 'gender',
            'last_name', 'first_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

"ログインフォーム"
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
