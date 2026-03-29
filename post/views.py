from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# 글 작성
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            title=title,
            content=content,
            image=image
        )
        return redirect('home')

    return render(request, 'write.html')


# 글 목록
def home(request):
    posts = Post.objects.all()
    return render(request, 'list.html', {'posts': posts})


# 글 상세
def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'post': post})
