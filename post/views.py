from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Photo
from .forms import PostForm

@login_required # 1. 로그인 확인
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # 2. post 객체를 만들 때 author(작성자)에 현재 유저(request.user)를 넣어줘!
        post = Post.objects.create(
            title=title, 
            content=content, 
            author=request.user
        )
        
        images = request.FILES.getlist('images')
        for img in images:
             Photo.objects.create(post=post, image=img)
    
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
@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 3. 작성자 본인인지 확인!
    if post.author != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("본인의 글만 수정할 수 있습니다.")

    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('post:detail', pk=post.pk)
    
    return render(request, 'post/update.html', {'post':post})

#5. 작성자 정보
@login_required 
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) 
            post.author = request.user      
            post.save()
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'post_form.html', {'form': form})
