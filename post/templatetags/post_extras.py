from django import template
import re


# tag 라이브러리를 만들기 위한 모듈 레벨의 인스턴스 객체
register = template.Library()

@register.filter
def add_link(value):
    content = value.content  # post의 content(내용)
    tags = value.tag_set.all()
    for tag in tags:
        # params in sub : 1. 찾고자 하는 패턴, 2. 바꾸려고 하는 형식, 3. 처음에 불러올 값
        content = re.sub(r'\#'+tag.name+r'\b', '<a href="/post/explore/tags/'+tag.name+'">#'+tag.name+'</a>', content)
    return content



