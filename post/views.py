from django.shortcuts import render, redirect
from .models import Post, Image

# Create your views here.
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(
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

def update(request, id):
    post = Post.objects.get(id = id)

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        return redirect(f'/detail/{post.id}/')
    
    return render(request, 'update.html', {'post' : post})
