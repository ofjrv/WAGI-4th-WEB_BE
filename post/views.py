import re #
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, PostImage, Comment

#목록
def home(request):
    query = request.GET.get('q', '').strip() 
    search_type = request.GET.get('type', 'all')
    
    if query:
        keywords = re.split(r'[\s,]+', query)
        keywords = [word for word in keywords if word]
        
        query_filter = Q()
        
        if keywords:
            first_word = keywords[0]
            if search_type == 'title':
                query_filter = Q(title__icontains=first_word)
            elif search_type == 'content':
                query_filter = Q(content__icontains=first_word)
            else:
                query_filter = Q(title__icontains=first_word) | Q(content__icontains=first_word)
            
            for word in keywords[1:]:
                if search_type == 'title':
                    query_filter |= Q(title__icontains=word)
                elif search_type == 'content':
                    query_filter |= Q(content__icontains=word)
                else:  # 'all'
                    query_filter |= (Q(title__icontains=word) | Q(content__icontains=word))
            
        posts = Post.objects.filter(query_filter).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
        
    return render(request, 'list.html', {
        'posts': posts, 
        'query': query, 
        'search_type': search_type
    })

#글쓰기 
@login_required(login_url='login')
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images') 
        
        post = Post.objects.create(author=request.user, title=title, content=content)
        
        for img in images:
            PostImage.objects.create(post=post, image=img)
            
        return redirect('home')
    return render(request, 'write.html')

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post': post})

#글수정
@login_required(login_url='login')
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.author != request.user:
        messages.error(request, "본인의 글만 수정할 수 있습니다.")
        return redirect('detail', post_id=post.id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        
        # [5주차 핵심] 기존 사진 삭제 (체크박스 선택된 것들)
        delete_image_ids = request.POST.getlist('delete_images')
        for img_id in delete_image_ids:
            img = get_object_or_404(PostImage, id=img_id)
            img.delete() # 모델 삭제 시 지우님이 만든 시그널이 파일도 지워줍니다.

        # [5주차 핵심] 새로운 사진 추가
        new_images = request.FILES.getlist('images')
        for img in new_images:
            PostImage.objects.create(post=post, image=img)
            
        post.save() 
        return redirect('detail', post_id=post.pk)
    
    return render(request, 'update.html', {'post': post})

#글삭제
@login_required(login_url='login')
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        messages.error(request, "본인의 글만 삭제할 수 있습니다.")
        return redirect('detail', post_id=post.id)
    post.delete()
    return redirect('home')

#좋아요 (M:N 관계)
@login_required(login_url='login')
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)
        is_liked = False
    else:
        post.likes.add(user)
        is_liked = True
        
    return JsonResponse({
        'is_liked': is_liked,
        'like_count': post.likes.count()
    })

@login_required(login_url='login') 
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        is_liked = False 
    else:
        comment.likes.add(request.user)    
        is_liked = True  
        
    return JsonResponse({
        'is_liked': is_liked,
        'like_count': comment.likes.count()
    })

#댓글작성 (1:N 관계)
@login_required(login_url='login')
def comment_write(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id') # 대댓글일 경우 부모 ID가 넘어옴

        if content:
            comment = Comment(post=post, author=request.user, content=content)
            if parent_id: # 부모 ID가 있다면 대댓글로 저장
                comment.parent_id = parent_id
            comment.save()
            
    return redirect('detail', post_id=post_id)

#댓글삭제
@login_required(login_url='login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if comment.author == request.user:
        comment.delete()
    else:
        messages.error(request, "본인 댓글만 삭제 가능합니다.")
    return redirect('detail', post_id=post_id)
