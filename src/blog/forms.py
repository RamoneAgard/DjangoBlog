from django import forms
from .models import BlogPost

class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
    # can overwrite model field
    # title = forms.CharField()
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date']

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data['title']
        instance = self.instance
        querySet = BlogPost.objects.filter(title__iexact=title)
        print(querySet)
        if instance is not None:
            print("hey")
            querySet = querySet.exclude(pk=instance.pk)
        if querySet.exists():
            raise forms.ValidationError("This title already exists.")
        return title
