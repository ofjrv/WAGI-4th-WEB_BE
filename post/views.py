from django.shortcuts import render, redirect, get_object_or_404
from .models import Post

# 1. 목록 (Home)
def home(request):
    posts = Post.objects.all().order_by('-created_at') # 최신순 정렬
    return render(request, 'list.html', {'posts': posts})

# 2. 글 쓰기 (Write)
def write(request):
    if request.method == 'POST':
        # formset 없이 직접 POST 데이터 가져오기
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image') # 파일은 FILES에서 가져와야 함
        
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

# + 삭제
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id) # 삭제할 글 찾기
    post.delete() # 데이터베이스에서 삭제
    return redirect('home') # 삭제 후 목록 페이지로 이동