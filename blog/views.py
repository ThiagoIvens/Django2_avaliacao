from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts' : posts})


def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		is_liked = True
	context = {
		'post' : post,
		'is_liked': is_liked,
		'total_likes': post.total_likes(),
	}

	return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})
	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def like_post(request):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(reques.user)
		is_liked = False
	else:
		post.likes.add(reques.user)
		is_liked = True
	post.likes.add(request.user)
	return HttpResponseRedirect(post.get_absolute_url())
