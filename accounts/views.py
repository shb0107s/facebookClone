from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm
from django.http import HttpResponse
import json
from chat.models import *


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login') # accounts 앱의 login으로 보낸다.
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_check(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(username=name, password=pwd)

        if user is not None:
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout(request):
    django_logout(request)
    return redirect("/")


def create_friend_request(request):
    user_id = request.POST.get('pk', None)
    user = request.user
    target_user = get_object_or_404(get_user_model(), pk=user_id)

    try:
        user.friend_requests.create(from_user=user, to_user=target_user)
        context = {'result': 'success'}
    except Exception as ex:
        print('에러가 발생했습니다.', ex)  # ex는 발생한 에러의 이름을 받아오는 변수
        context = {'result': 'error'}

    return HttpResponse(json.dumps(context), content_type="application/json")

def accept_friend_request(request):
    friend_request_id = request.POST.get('pk', None)

    # 요청 불러오기
    friend_request = FriendRequest.objects.get(pk=friend_request_id)

    # current user 가져오기
    from_user = friend_request.from_user

    # target user 가져오기
    to_user = friend_request.to_user

    try:
        # 친구관계 생성
        # 채팅방 이름 생성
        room_name = f"{from_user.username},{to_user.username}"

        # 채팅방 생성
        #room = Room.objects.create(room_name=room_name)
        Friend.objects.create(user=from_user, current_user=to_user) #, room=room)
        Friend.objects.create(user=to_user, current_user=from_user) #, room=room)

        # 작업완료된 친구요청을 삭제
        friend_request.delete()

        context = {'result': 'success'}

    except Exception as ex:
        print("에러가 발생했습니다.", ex)
        context = {'result': 'error'}

    return HttpResponse(json.dumps(context), content_type="application/json")
