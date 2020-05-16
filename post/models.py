from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re

from accounts.models import *


# Create your models here.
def photo_path(instance, filename):
    from time import strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extention = filename.split('.')[-1]
    return f"{strftime('post/%Y/%m/%d/')}/{instance.author.username}/{pid}.{extention}"


class Post(models.Model):
    # admin 페이지에서 로그인했던 유저모델을 그대로 가져와서 사용
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # on_delete=models.CASCADE : 유저 모델이 삭제되면 author도 삭제됨

    photo = ProcessedImageField(upload_to=photo_path,
                                processors=[ResizeToFill(600,600)],
                                format='JPEG',
                                options={'quality': 90})
    
    content = models.CharField(max_length=140, help_text="최대 140자 입력 가능")
    
    # auto_now=True는 django model이 save될 때마다 현재날짜(date.today()) 로 갱신.
    # auto_now_add=True는 django model이 최초 저장(insert)시에만 현재날짜(date.today()) 를 적용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           blank=True,  # 기존에 만들었던 모델에 새로운 필드를 추가할 때는 blank=True를 줘야 문제가 생기지 않는다.
                                           related_name='like_post_set',  # 나중에 이 이름으로 찾을 수 있다.
                                           through='Like')  # Like class와 연결

    bookmark_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                               blank=True,
                                               related_name='bookmark_post_set',
                                               through='Bookmark')

    class Meta:
        ordering = ['-created_at']

    @property
    def like_count(self):
        return self.like_user_set.count()

    @property
    def bookmark_count(self):
        return self.bookmark_user_set.count()


    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 클래스 전체의 규칙을 정한다.
        unique_together = (
            ('user', 'post')
        )


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 클래스 전체의 규칙을 정한다.
        unique_together = (
            ('user', 'post')
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_set')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.content

