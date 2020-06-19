from django import forms
from .models import BlogComment

class BlogCommentModelForm(forms.ModelForm):
    content = forms.CharField(
        max_length = 300,
        label = False,
        widget = forms.Textarea(attrs={
                        'class':'mb-0 rounded',
                        'rows':2,
                        'cols':50,
                        'maxlength':300,
                        'placeholder':"Comment on this Post.."}))
    class Meta:
        model = BlogComment
        fields = ['content']
