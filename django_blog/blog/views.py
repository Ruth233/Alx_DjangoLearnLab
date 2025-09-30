from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm
from .forms import CommentForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after register
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    # Edit email if POST
    if request.method == 'POST':
        email = request.POST.get('email')
        if email and email != request.user.email:
            request.user.email = email
            request.user.save()
    return render(request, 'blog/profile.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # blog/templates/blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10                         # optional

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'                      # redirect if not logged in

    def form_valid(self, form):
        # set the author to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Create a comment under a given post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        # capture post for later use
        self.post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return self.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user
