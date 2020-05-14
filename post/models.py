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

    def __str__(self):
        return self.content



