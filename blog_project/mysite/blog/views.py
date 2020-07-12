from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

# This view will list all the Posts that were made.
class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

# This view will show all the details of a particular post, it accepts primary key internally.
class PostDetailView(DetailView):
    model = Post


# LoginRequiredMixin is used to check if the user has logen in or not to create the post.
class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/' # If the user is not loged in then this line will ask the user to login.
    redirect_field_name = 'blog/post_detail.html' # After the user logs in sucessfully, this line will redirect to the required page.
    form_class = PostForm
    model = Post

# LoginRequiredMixin is used to check if the user has logen in or not to create the post.
class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/' # If the user is not loged in then this line will ask the user to login.
    redirect_field_name = 'blog/post_detail.html'  # After the user logs in sucessfully, this line will redirect to the required page.
    form_class = PostForm
    model = Post

# LoginRequiredMixin is used to check if the user has logen in or not to create the post.
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list') # It will take the userback to post_list view after deleting the post.

# LoginRequiredMixin is used to check if the user has logen in or not to create the post.
class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'  # After the user logs in sucessfully, this line will redirect to the required page.
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

##############################################################################################################################
##############################################################################################################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk) 
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk) # If it gets the post object with the primary key or returns 404 not found.
    if request.method == 'POST':
        form = CommentForm(request.POST) # creates form as a CommentForm object
        if form.is_valid():
            comment = form.save(commit = False) # Saves the comment form's data into comment without commitimg.
            comment.post = post # Sets the comment to the respective post.
            comment.save() # Saves the comment by auto commiting.
            return redirect('post_detail',pk=post.pk) # Redirects to the PostDetails page for that particular post.
    else:
        form = CommentForm() # It will ask to fill the comment form again.
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)