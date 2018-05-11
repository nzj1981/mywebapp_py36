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
from core.handlers.handler import get_page_index, check_admin
from db.models.model import Comment, Blog


@get('/api/comments')
async def api_comments(request, *, page='1'):
    page_index = get_page_index(page)
    user = request.__user__
    if user.admin == 1:
        num = await Comment.findNumber('count(id)')
    else:
        num = await Comment.findNumber('count(id)', where='user_id=?', args=(user.id,))
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    if user.admin == 1:
        comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    else:
        comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit), where='user_id=?', args=[user.id])
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


# 评论列表管理
@get('/manage/')
def manage():
    return 'redirect:/manage/comments'


@get('/manage/comments')
def manage_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page),
        'title': '评论管理'
    }


# 评论删除
@post('/api/comments/{id}/delete')
async def api_delete_comments(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceNotFoundError('Comment', 'Comment content is empty.')
    await c.remove()
    return dict(id=id)