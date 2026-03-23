from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# 1. 목록 (list)
def list(request):
    posts = Post.objects.all().order_by('-id') #최신순 정렬
    return render(request, 'list.html', {'posts': posts})

# 2. 상세 (detail)
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'detail.html', {'post': post})

# 3. 작성 (write)
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

        return redirect('list')
    
    return render(request, 'write.html')