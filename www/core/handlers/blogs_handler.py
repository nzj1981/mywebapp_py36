# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: blogs_handler.py
@time: 2018/4/25 16:08
"""

__author__ = 'autumner'

'''
blogs handlers
'''


import markdown2
from coroweb import get, post
from db.models.model import Comment, Blog
from checks.apis import APIValueError, Page
from core.handlers.handler import text2html, get_page_index, check_admin


# blogs of index
@get('/')
async def index(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    page = Page(num, page_index)
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))

    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs
    }


# blog to page
@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }


# 日志的管理页面
@get('/manage/blogs')
def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page),
        'title': '日志管理'
    }


# blog to create of get
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs',
        'title': '日志管理'
    }



# blogs list page
@get('/api/blogs')
async def api_blogs(request, *, page='1'):
    page_index = get_page_index(page)
    user = request.__user__
    if user.admin == 1:
        num = await Blog.findNumber('count(id)')
    else:
        num = await Blog.findNumber('count(id)', where='user_id=?', args=(user.id))
    p = Page(num, page_index)

    if num == 0:
        return dict(page=p, blogs=())
    if user.admin == 1:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    else:
        blogs = await Blog.findAll(
            where='user_id=?',
            args=[user.id],
            orderBy='created_at desc',
            limit=(p.offset, p.limit)
        )

    return dict(page=p, blogs=blogs)



# blog to show of get
@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog



# 日志编辑页面
@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }


# blog to edit of post
@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')

    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image, name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


# blog to update of post
@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = await Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')

    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()

    await blog.update()

    return blog


# blog to delete of post
@post('/api/blogs/{id}/delete')
async def api_delete_blog(request, *, id):
    check_admin(request)
    blog = await Blog.find(id)
    await blog.remove()
    return dict(id=id)

