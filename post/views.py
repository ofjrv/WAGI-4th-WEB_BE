from django.shortcuts import render, redirect
from .models import Post

# Create your views here.
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            title = title, 
            content = content, 
            image = image
        )
        return redirect('home')
    
    return render(request, 'write.html')

def home(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'list.html', {'posts' : posts})

def detail(request, post_id):
    post = Post.objects.get(id = post_id)
    return render(request, 'detail.html', {'post' : post})