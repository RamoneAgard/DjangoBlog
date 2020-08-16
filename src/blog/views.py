from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from .models import BlogPost
from .forms import BlogPostModelForm
from comments.models import BlogComment
from comments.forms import BlogCommentModelForm

def blog_post_detail_page(request, slug):
    # obj = BlogPost.objects.get(id=post_id)
    obj = get_object_or_404(BlogPost, slug=slug)
    '''
    or
    try:
        obj = BlogPost.objects.get(id=post_id)
    except BlogPost.DoesNotExist:
        raise Http404
    except ValueError
        raise Http404
    '''
    # (if no unique identifier or other non-unique filter)
    #
    # querySet = BlogPost.objects.filter(slug = slug)
    # if querySet.count() == 0:
    #     raise Http404
    #
    # obj = querySet.first()

    template_name = 'blog_post_detail.html'
    context = {"object": obj}
    return render(request, template_name, context)

'''
CRUD -- Create, Retrieve, Update, Delete
'''


def blog_post_list_view(request):
    # list out objects, could be search
    querySet = BlogPost.objects.all().published()
    # or objects.published() --> list of objects
    context = {}
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        querySet = (querySet | my_qs).distinct()
        form = BlogCommentModelForm() # form for comments
        if request.method == 'POST':
            form = BlogCommentModelForm(request.POST or None)
            if form.is_valid():
                comment = form.save(commit=False)
                comment_post_slug = request.POST.get('blog_slug')
                comment_post = querySet.filter(slug=comment_post_slug).first()
                comment.blog_post = comment_post
                comment.user = request.user
                comment.save()
        context["comment_form"] = form
    PostCommentList = []
    for bp in querySet:
        coms = bp.comments.all()
        if coms.count() > 5:
            coms = coms[:5]
        b_c_set = (bp, coms)
        PostCommentList.append(b_c_set)
    template_name = 'blog/list.html'
    context["object_list"] =  PostCommentList
    return render(request, template_name, context)

@login_required # need to be logged in
@staff_member_required # need staff permissions -- forced to login to django admin
def blog_post_create_view(request):
    # create objects/post_id
    # uses a form
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # print(form.cleaned_data)
        # form.save()
        # or
        obj = form.save(commit=False)
        obj.user = request.user # --> must have a value
        obj.save()
        # obj = BlogPost.objects.create(**form.cleaned_data) for non-model forms
        form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'title': "New Blog Post",
        "form": form}
    return render(request, template_name, context)

def blog_post_detail_view(request, slug):
    # 1 object is retrieved -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    context = {}
    if request.user.is_authenticated:
        comment_form = BlogCommentModelForm()
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
    coms = obj.comments.all()
    if coms.count() > 5:
        coms = coms[:5]
    template_name = 'blog/detail.html'
    context["object"] = obj
    context["object_comments"] = coms
    return render(request, template_name, context)

def blog_post_update_view(request, slug):
    # update object/post
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    if request.method == 'POST':
        return redirect(f"/blog/{slug}")
    template_name = 'form.html'
    context = {"object": obj, "form": form, "title": f"Update {obj.title}"}
    return render(request, template_name, context)

def blog_post_delete_view(request, slug):
    # delete object/post
    obj = get_object_or_404(BlogPost, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect("/blog")
    template_name = 'blog/delete.html'
    context = {"object": obj}
    return render(request, template_name, context)
