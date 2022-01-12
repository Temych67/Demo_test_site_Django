from django import forms
from data_app.models import DataModels


class CreateDataPostForm(forms.ModelForm):
    class Meta:
        model = DataModels
        fields = ['title', 'body']


class UpdateDataPostForm(forms.ModelForm):
    class Meta:
        model = DataModels
        fields = ['title', 'body']

    def save(self, commit=True):
        data_post = self.instance
        data_post.title = self.cleaned_data['title']
        data_post.body = self.cleaned_data['body']

        if commit:
            data_post.save()
        return data_post