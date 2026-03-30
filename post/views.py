from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# 1. 목록 (Home)
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'posts': posts})

# 2. 글 쓰기 (Write) - 이 부분이 에러의 핵심입니다!
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # [수정] image_url 대신 실제 파일(FILES)을 가져옵니다.
        image = request.FILES.get('image') 
        
        # [수정] 데이터베이스의 image 칸에 파일을 저장합니다.
        Post.objects.create(
            title=title,
            content=content,
            image=image
        )
        return redirect('home')
    return render(request, 'write.html')

# 3. 상세 보기 (Detail)
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post': post})

# 4. 삭제
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('home')