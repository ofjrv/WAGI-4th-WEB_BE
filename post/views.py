from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Photo

def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        post = Post.objects.create(title=title, content=content)
        
        images = request.FILES.getlist('images')

        for img in images:
             Photo.objects.create(post=post, image=img) # Post 대신 Photo!
    
        return redirect('post:list')
        
    return render(request, 'post/write.html')

# 2. 목록 보기
def list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/list.html', {'posts': posts})

# 3. 상세보기
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/detail.html', {'post': post})

# 4. 수정한 내용 불러오기
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':

        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('post:detail', pk=post.pk)
    
    return render(request, 'post/update.html', {'post':post})
