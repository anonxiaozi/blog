from django.forms import fields, widgets, ModelForm, Form
from .models import Blog
import os
from django.forms import fields, widgets
from django.core.exceptions import ValidationError
import uuid
from django.conf import settings


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ['content']

    def clean_background_img(self):
        accept_type = ['.jpg', '.png', '.jpeg']
        img = self.cleaned_data['background_img']
        if os.path.splitext(img)[-1] not in accept_type:
            raise ValidationError('不支持的文件类型', code=500)
        else:
            return img


class EmailForm(Form):
    name = fields.CharField(max_length=50)
    phone = fields.IntegerField(max_value=99999999999, error_messages={'max_value': 'invalid phone number.'})
    email = fields.CharField(max_length=80, widget=fields.EmailInput)
    message = fields.CharField(max_length=1024 * 1024, widget=fields.TextInput)
