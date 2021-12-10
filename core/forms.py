from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, TextInput
from django import forms
from core.models import DataSetModel,ColumnModel,TableModel
from django.forms import inlineformset_factory



row_formset = inlineformset_factory(TableModel, ColumnModel,fields=('name', 'column_type', 'order', 'range_from', 'range_to'),
            labels={'name': 'Column name', 'column_type': 'Type',
                    'order': 'Order', 'range_from': 'From', 'range_to': 'To'},
            can_order=False, can_delete=True
        )

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        exclude = ['email', 'is_superuser', 'is_staff']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(size='16', placeholder='Username')
        self.fields['password'].widget.attrs.update(size='16', placeholder='Password')


class Table_Form(ModelForm):
    class Meta:
        model=TableModel
        fields = 'name','column_separator','string_character'


class DataSetForm(ModelForm):
    class Meta:
        model = DataSetModel
        fields = ['rows']
