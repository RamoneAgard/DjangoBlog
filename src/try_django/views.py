from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from blog.models import BlogPost
from comments.models import BlogComment
from comments.forms import BlogCommentModelForm

def home_page(request):
    my_title = "Welcome to the Blog"
    context = {}
    querySet = BlogPost.objects.all()
    if request.user.is_authenticated:
        comment_form = BlogCommentModelForm()
        my_title = "Welcome Back to the Blog:"
        if request.method == 'POST':
            comment_form = BlogPostModelForm(request.POST or None)
            if form.is_valid():
                comment = form.save(commit=False)
                comment_post_slug = request.POST.get('blog_slug')
                comment_post = querySet.filter(slug=comment_post_slug).first()
                comment.blog_post = comment_post
                comment.user = request.user
                comment.save()
        context["comment_form"] = comment_form
    PostCommentList = []
    for bp in querySet:
        coms = bp.comments.all()
        if coms.count() > 5:
            coms = coms[:5]
        b_c_set = (bp, coms)
        PostCommentList.append(b_c_set)
    context["object_list"] = PostCommentList
    context["title"] = my_title
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
