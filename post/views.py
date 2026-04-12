from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostImage

# 글 작성
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')

        post = Post.objects.create(
            title=title,
            content=content
        )

        for img in images:
            PostImage.objects.create(post=post, image=img)

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

#글 수정
def update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('detail', id=post.id)

    return render(request, 'update.html', {'post': post})