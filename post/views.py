from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import *

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json


# Create your views here.
def post_list(request):
    post_list = Post.objects.all()

    if request.user.is_authenticated:
        username = request.user

        friends = username.friends.all()  # 친구 목록
        request_friends = username.friends_requests  # 친구 요청 목록

        user = get_object_or_404(get_user_model(), username=username)

        # accounts/models.py의 class Profile에서 settings.AUTH_USER_MODEL을 통해서
        # 장고가 기본으로 제공하는 user와 model을 Profile에서 획장해서 쓰고 있기 때문에
        # profile에 있는 정보들에 접근할 수 있다.
        user_profile = user.profile

        friend_list = user.friends.all()
        my_friends_user_list = list(map(lambda friend: friend.user, friend_list))
        # map : 리스트로부터 원소를 하나씩 꺼내서 함수를 적용시킨 다음, 그 결과를 새로운 리스트에 담아줌
        
        friend_request_list = user.friends_requests.all()
        my_friend_request_user_list = list(map(lambda friend_request: friend_request.to_user, friend_request_list))

        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': post_list,
            'friends': friends,
            'request_friends': request_friends,
            'my_friends_user_list': my_friends_user_list,
            'my_friend_request_user_list': my_friend_request_user_list,
        })

    else:
        return render(request, 'post/post_list.html', {'posts': post_list,})


@login_required  # 로그인된 상태에서만
@require_POST  # POST로만 값을 받을 수 있게
def post_like(request):
    pk = request.POST.get('pk', None)  # pk값은 ajax 통신을 통해 받는다.
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:  # 생성된 좋아요가 없다면
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
                'message': message}
    
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def post_bookmark(request):
    pk = request.POST.get('pk', None)  # pk값은 ajax 통신을 통해 받는다.
    post = get_object_or_404(Post, pk=pk)
    post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(user=request.user)

    if not post_bookmark_created:  # 생성된 좋아요가 없다면
        post_bookmark.delete()
        message = "북마크 취소"
        is_bookmarked = 'N'
    else:
        message = "북마크"
        is_bookmarked = 'Y'

    context = {'is_bookmarked': is_bookmarked,
                'message': message}
    
    return HttpResponse(json.dumps(context), content_type="application/json")
