from django.shortcuts import render, redirect

from posts.forms import PostCreateForm, CommentCreateForm
from posts.models import Post, Comment
from posts.constans import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView


# Create your views here.


# def main_page_view(request):
#     if request.method == 'GET':
#         return render(request, 'layouts/index.html')


class MainPageCBV(ListView):
    model = Post


# def posts_view(request):
#     if request.method == 'GET':
#         posts = Post.objects.all().order_by('-rate', 'created_date')
#         search = request.GET.get('search')
#         page = int(request.GET.get('page', 1))
#
#         ''' start_with, ends_with, icontains '''
#
#         '''and | or'''
#
#         if search:
#             posts = posts.filter(title__icontains=search) | posts.filter(description__icontains=search)
#
#         max_page = posts.__len__() / PAGINATION_LIMIT
#         max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)
#
#         ''' posts splice'''
#         posts = posts[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]
#
#         context = {
#             'posts': posts,
#             'user': request.user,
#             'pages': range(1, max_page + 1)
#         }
#
#         return render(request, 'posts/posts.html', context=context)


class PostsCBV(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'

    def get(self, request, **kwargs):
        posts = self.get_queryset().order_by('-rate', 'created_date')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        ''' start_with, ends_with, icontains '''

        if search:
            posts = posts.filter(title__icontains=search)
        max_page = posts.__len__() / PAGINATION_LIMIT
        max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)

        ''' posts splice'''
        posts = posts[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'posts': posts,
            'user': request.user,
            'pages': range(1, max_page + 1)
        }

        return render(request, self.template_name, context=context)


def post_detail_view(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)

        context = {
            'post': post,
            'comments': post.comment_set.all(),
            'form': CommentCreateForm
        }

        return render(request, 'posts/detail.html', context=context)

    if request.method == 'POST':
        post = Post.objects.get(id=id)
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                post_id=id
            )

        context = {
            'post': post,
            'comments': post.comment_set.all(),
            'form': form,
            'user': request.user,
        }

        return render(request, 'posts/detail.html', context=context)


# def post_create_view(request):
#     if request.method == 'GET':
#         context = {
#             'form': PostCreateForm
#         }
#         return render(request, 'posts/create.html', context)
#
#     if request.method == 'POST':
#         form = PostCreateForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             Post.objects.create(
#                 title=form.cleaned_data.get('title'),
#                 description=form.cleaned_data.get('description'),
#                 rate=form.cleaned_data.get('rate'),
#                 image=form.cleaned_data.get('image')
#             )
#             return redirect('/posts/')
#
#         return render(request, 'posts/create.html', context={'form': form})


class PostCreateCBV(ListView, CreateView):
    model = Post
    template_name = 'posts/create.html'
    form_class = PostCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate'),
                image=form.cleaned_data.get('image')
            )
            return redirect('/posts/')

        return render(request, self.template_name, context=self.get_context_data(form=form))
