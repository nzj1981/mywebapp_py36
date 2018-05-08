# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: comments_handler.py
@time: 2018/5/7 13:15
"""

__author__ = 'autumner'

'''
comments handlers
'''


from coroweb import get, post
from checks.apis import Page, APIValueError, APIPermissionError, APIResourceNotFoundError
from core.handlers.handler import get_page_index
from db.models.model import Comment, Blog



@get('/api/comments')
async def api_comments(*, page='1'):
    page_index = get_page_index(page)
    num = await Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)


@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please sigin first.')
    if not content or not content.strip():
        raise APIValueError('content', 'comments content cannot be empty.')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog', 'Blog resource cannot be empty.')
    comment = Comment(
        blog_id=blog.id,
        user_id=user.id,
        user_name=user.name,
        user_image=user.image,
        content=content.strip()
    )
    await comment.save()
    return comment


