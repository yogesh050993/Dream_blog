from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author, PostView
from .forms import CommentForm, PostForm
from marketing.models import SignUp
from marketing.forms import EmailSignupForm
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    View, ListView, DetailView, UpdateView, CreateView, DeleteView
)

form = EmailSignupForm()

def get_author(user):
    query = Author.objects.filter(user=user)
    if query.exists():
        return query[0]
    return None

class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset,
        }
        return render(request, 'search_results.html', context)


def get_category_count():
    quertset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return quertset


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        first_three = Post.objects.order_by('timestamp')[:3]
        latest_posts = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'object_list': featured,
            'latest': latest_posts,
            'form': self.form,
            'first_three' : first_three,
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()
        return redirect("index")


class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_variable'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=obj)
        return obj


    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_variable'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            post = self.get_object()
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'pk': post.pk,
            }))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context


    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = get_author(self.request.user)
            form.save()
            # return super().form_valid(form)
            return redirect(reverse("post-detail", kwargs={
                'pk' : form.instance.pk
            }))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = get_author(self.request.user)
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': form.instance.pk
            }))


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = "/blog"


def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    return render(request, 'account/profile.html')

