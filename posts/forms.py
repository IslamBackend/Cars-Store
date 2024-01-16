from django import forms


class PostCreateForm(forms.Form):
    image = forms.FileField(required=False)
    rate = forms.FloatField(required=False)
    title = forms.CharField(max_length=255, min_length=6)
    description = forms.CharField(widget=forms.Textarea())


class CommentCreateForm(forms.Form):
    text = forms.CharField(max_length=255, min_length=3)
