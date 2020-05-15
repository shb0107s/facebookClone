from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re  # regular expressions

# Create your models here.

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = "".join(arr)  # join function : 리스트를 특정 구분자를 포함해 문자열로 변환하는 함수 cf)split
    extension = filename.split('.')[-1]
    return f"accounts/{instance.user.username}/{pid}.{extension}"


class Profile(models.Model):
    # 1:1로 관계를 맺는다.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # on_delete=models.CASCADE => 어느 한쪽이라도 삭제가 되면 반대쪽도 삭제되도록(1:1관계이므로)
    
    #field 생성
    # CharField는 max_length가 필수 값
    nickname = models.CharField('별명', max_length=30, unique=True)
    picture = ProcessedImageField(upload_to=user_path, 
                        processors=[ResizeToFill(150,150)],
                        format='JPEG',
                        options={'quality': 90},
                        blank=True)

    about = models.CharField(max_length=300, blank=True)

    GENDER_C = (
        ('선택안함', '선택안함'),
        ('여성', '여성'),
        ('남성', '남성'),
    )

    gender = models.CharField('성별(선택사항)',
                     max_length=10,
                     choices=GENDER_C,
                     default='N')


class Friend(models.Model):
    # 상대방
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)
    # room = models.ForeignKey(Room, blank=True, on_delete=models.SET_NULL, null=True)

    # 현재 로그인한 나
    # related_name은 friend 클래스를 바라볼 때 쓸 수 있는 이름. 일종의 주소
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friends', blank=True, on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username  # username이 Friend의 대표값이 된다.


# 친구 요철을 보내고 받는 모델 생성
class FriendRequest(models.Model):
    # 요청을 보내는 쪽
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friend_requests', on_delete=models.CASCADE)

    # 요청을 받는 쪽
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requested_friend_requests', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"

    class Meta:
        unique_together = (
            ('from_user', 'to_user')
        )






