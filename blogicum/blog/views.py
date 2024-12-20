from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)
from django.http import Http404

from .models import Post, Category, Comment, User
from blog.forms import PostForm, CommentForm, ProfileUpdateForm


class PostListView(ListView):
    """Отображения списка постов."""
    template_name = 'blog/index.html'
    model = Post
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True).select_related('author')
        return queryset


class PostDetailView(UserPassesTestMixin, DetailView):
    """Отображение конкретного поста."""
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def test_func(self):
        # проверяем, является ли текущий
        # пользователь автором редактируемого поста
        post = self.get_object()
        return self.request.user == post.author or post.is_published

    def handle_no_permission(self):
        raise Http404

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.test_func():
            return self.handle_no_permission()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        post = self.get_object()
        context['comments'] = post.comments.all()
        return context


class CategoryPost(ListView):
    """Отображения списка категорий."""
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        category_slug = self.kwargs['slug']
        self.category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )

    def get_queryset(self):
        return self.category.post_set.filter(
            pub_date__lte=timezone.now(),
            is_published=True
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProfileListView(ListView):
    """
    Просмотр профиля
    """
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        posts = user.post_set.all().order_by('-pub_date')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = user
        context['page_number'] = self.request.GET.get('page')
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование профиля, требующее логина (миксин)
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'blog/user.html'

    def check_user_authorization(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_object(self, *args, **kwargs):
        return self.request.user

    def form_valid(self, form):
        response = super(ProfileUpdateView, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.get_username()})


class CreatePostView(LoginRequiredMixin, CreateView):
    """Создание поста, требующее логина (миксин)."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.get_username()})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование поста, которое требует логина и разрешений."""
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def test_func(self):
        # проверяем, является ли текущий
        # пользователь автором редактируемого поста
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return redirect('blog:detail', post_id=post.id)

    def get_success_url(self):
        return reverse_lazy('blog:detail',
                            kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление поста, которое требует логина"""
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def has_permission(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария к посту, требующее логина (миксин)."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=kwargs['post_id'])
        return context

    def get_success_url(self):
        return reverse_lazy(
            'blog:detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class EditCommentView(LoginRequiredMixin, UpdateView):
    """Редактирование комментария, , требующее логина (миксин)"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'blog:detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    """Удаление комментария, требующее логина (миксин)"""
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            'blog:detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
