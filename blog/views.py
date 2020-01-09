from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.views.generic.dates import MonthArchiveView
from .models import Post, Comment
from markdown import markdown
from django import forms
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'content',)


class PostDetailDisplay(DetailView):
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['new_comment_form'] = PostCommentForm()
        return context


class PostCommentAction(SingleObjectMixin, FormView):
    template_name = 'blog/post_detail.html'
    form_class = PostCommentForm
    model = Post
    extra_content = 'posts'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.object.pk)
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return super().form_valid(form)


class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentAction.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        title_match = Post.objects.filter(title__icontains=query)
        content_match = Post.objects.filter(content__icontains=query)
        author_match = Post.objects.filter(author__username__icontains=query)
        return (title_match | content_match | author_match).distinct().order_by('-date_posted')


class PostMonthArchiveView(MonthArchiveView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.all()
    date_field = "date_posted"
    allow_future = True
    paginate_by = 5


class TagView(ListView):
    model = Post
    template_name = 'blog/tag_view.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag = self.kwargs.get('tagname')
        return Post.objects.filter(tags__name__in=[tag])

    def get_context_data(self, *args, **kwargs):
        tag=self.kwargs.get('tagname')
        context = super().get_context_data(*args, **kwargs)
        context['tagname'] = tag
        context['total_num_posts'] = len(Post.objects.filter(tags__name__in=[tag]))
        return context


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})