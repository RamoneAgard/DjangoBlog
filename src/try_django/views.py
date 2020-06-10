from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
    my_title = "Welcome to My Blog"
    context = {"title": my_title}
    querySet = BlogPost.objects.all()
    context["blog_list"] = querySet
    # doc = "<h1>{title}</h1>".format(title=my_title)
    # django_rendered_doc = "<h1>{{title}}</h1>".format(title=my_title)
    return render(request, "home.html", context)

def about_page(request):
    return render(request, "about.html", {"title": "About Us"})

def contact_page(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {"title": "Contact Us",
        "form": form}
    return render(request, "form.html", context)

def example_page(request):
    context = {"title": "Example"}
    template_name = "hello_world.html"
    #template_obj = get_template(template_name)
    #rendered_item = template_obj.render(context)
    return render(request, template_name, context)
