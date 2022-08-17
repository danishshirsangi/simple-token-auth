from django.forms import ModelForm
from .models import UserCustom, DonorDonee


class UserAddForm(ModelForm):
    class Meta:
        model = UserCustom
        exclude = ['last_login']
