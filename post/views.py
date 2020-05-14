from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import *


# Create your views here.
def post_list(request):
    post_list = Post.objects.all()

    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)

        # accounts/models.py의 class Profile에서 settings.AUTH_USER_MODEL을 통해서
        # 장고가 기본으로 제공하는 user와 model을 Profile에서 획장해서 쓰고 있기 때문에
        # profile에 있는 정보들에 접근할 수 있다.
        user_profile = user.profile
        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': post_list,
        })

    else:
        return render(request, 'post/post_list.html', {'posts': post_list,})
