from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # 데이터 저장 (image 오타 주의!)
        Post.objects.create(title=title, content=content, image=image)
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