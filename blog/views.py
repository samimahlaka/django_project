from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.models import Post
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ( ListView , 
DetailView, 
CreateView,
UpdateView,
DeleteView
)
from django.contrib import messages

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
    paginate_by = 5;

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
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post;
    fields = ['title', 'content'];
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        form.instance.author = self.request.user;
        messages.success(self.request,f'Post has been updated')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object();
        if self.request.user == post.author:
            return True;
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post;
    context_object_name = 'post'
    success_url = reverse_lazy('blog-home');


    def test_func(self):
        post = self.get_object();
        if self.request.user == post.author:
            return True;
        else:
            return False;

        
def about(request):
    return render(request, 'blog/about.html', {'title' : 'BlogAbout'});