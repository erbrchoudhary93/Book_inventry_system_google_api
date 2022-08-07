from django import forms
from .models import Store, Books
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Add_Store(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["store_name","loc"]

        labels = {'store_name': 'Store Name',
                  'loc': 'Location'}
        widgets= {
            'store_name':forms.TextInput({'class':'form-control','placeholder':'Enter Your Store Name'}),
            'loc':forms.TextInput(attrs={'class':"form-control",'placeholder':"Enter Your Store Location"})
            }
       
 


class Edit_Book(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['bookname','count']
        labels = {'bookname': 'Title of book',
                  'count': 'No. of book'}
        widgets= {
        'bookname':forms.TextInput({'class':'form-control'}),
        'count':forms.TextInput({'class':"form-control",'placeholder':"Enter Your Store Location"})
        }

class Search(forms.Form):
    search = forms.CharField(max_length=1000)
    



        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username','email','password1','password2']