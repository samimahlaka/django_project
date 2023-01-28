from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView, CreateView

context = {
    'posts': Post.objects.all()
}
def home(request):
    return render(request, 'blog/home.html',context);

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/home.html'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post;
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post;
    fields = ['title', 'content']
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



def about(request):
    return render(request, 'blog/about.html', {'title' : 'BlogAbout'});