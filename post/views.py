from django.shortcuts import render, redirect
from .models import Post, Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        post = Post.objects.create(
            author = request.user,
            title = title, 
            content = content
        )
        images = request.FILES.getlist('images')

        for img in images:
            Image.objects.create(
                post = post,
                image = img
            )
        
        return redirect('home')
    
    return render(request, 'write.html')

def home(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'list.html', {'posts' : posts})

def detail(request, post_id):
    post = Post.objects.get(id = post_id)
    return render(request, 'detail.html', {'post' : post})

@login_required
def update(request, id):
    post = Post.objects.get(id = id)

    if post.author != request.user:
        return HttpResponseForbidden("수정 권한 없음")

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        return redirect(f'/detail/{post.id}/')
    
    return render(request, 'update.html', {'post' : post})