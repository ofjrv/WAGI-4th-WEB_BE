from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostImage

# 1. 목록 (Home)
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'posts': posts})

# 2. 글 쓰기 (다중 이미지 처리)
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # name="images"로 들어오는 모든 파일을 리스트로 가져옵니다.
        images = request.FILES.getlist('images') 
        
        # 게시글 생성
        post = Post.objects.create(title=title, content=content)
        
        # 파일들을 하나씩 꺼내서 PostImage 객체로 생성
        for img in images:
            PostImage.objects.create(post=post, image=img)
            
        return redirect('home')
    return render(request, 'write.html')

# 3. 상세 보기
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post': post})

# 4. 수정 (Update)
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save() 
        return redirect('detail', post_id=post.pk)
    
    # 수정 페이지로 기존 데이터를 넘겨줍니다.
    return render(request, 'update.html', {'post': post})

# 5. 삭제
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete() # 연관된 PostImage와 파일들도 함께 삭제됩니다.
    return redirect('home')