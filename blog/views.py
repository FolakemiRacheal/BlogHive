from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post, Comment, Like

# Create your views here.



#Function BaseView
def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/home.html', context)



#classbaseview
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name='posts'
    ordering = ['-date_posted']
    paginate_by = 2



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name='posts'
    # ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    



class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    

    def test_func(self):
        post = self.get_object()
        if self.request.user ==post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
        model = Post
        success_url = '/'


        def test_func(self):
            post = self.get_object()
            if self.request.user ==post.author:
                return True
            return False


def about(request):
    return render(request, 'blog/about.html')



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
    
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            return redirect("post_detail", pk=post.pk)

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "is_liked": is_liked,
    })

@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(post=post, user=request.user)
    if like.exists():
        like.delete()
    else:
        Like.objects.create(post=post, user=request.user)
    return redirect("post_detail", pk=pk)