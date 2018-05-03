# mywebapp_py36
把所有学到python知识整合成一个python版web项目

一、创建一个python的web项目

项目名称：
    
        mywebapp_py36

开发工具：
 
          Anaconda3-5.1.0-Linux-x86_64.sh
          pycharm-2017.3
          git1.8.3
          github
github地址:

    https://github.com/nzj1981/mywebapp_py36.git
    
创建虚拟环境:
 
    myweb_py36
    
创建命令:

    conda create --name myweb_py36 python=3.6


激活环境:
      
        activate myweb_py36
    
二、项目结构及安装第三方库


2.1.项目结构


    mywebapp_py36/    <-根目录
    |
    +--backup/        <-备份目录
    |
    +--dist/          <-打包目录
    |
    +--www/           <-Web目录,存放.py文件
    | |
    | +--static/      <-存放静态文件
    | |
    | +--templates/   <-存放模板文件
    |
    +--ios/           <-存放IOS App工程
    |
    +--android/       <-存放Android App工程
    |
    +--LICENSE        <-代码LICENSE
 
    
2.2.安装第三方库

    A.异步框架 aiohttp
    
    B.前端模板引擎 jinja2
    
    C.MySQL的Python异步驱动程序 aiomysql

安装命令：

    conda install aiohttp
    conda install jinja2
    pip install aiomysql
    pip install asyncio
查看已安装的第三方库

    conda list
    
三、创建数据库与表

3.1 创建库

root用户:

    drop database if exists awesome;
    create database awesome;
    use awesome;
    Grant all privileges on awesome.* to 'pyuser'@'%' identified by 'pyuser123' with grant option;
    flush privileges;

3.2 创建表

pyuser用户：

    create table users (
        `id` varchar(50) not null,
        `email` varchar(50) not null,
        `passwd` varchar(50) not null,
        `admin` bool not null,
        `name` varchar(50) not null,
        `image` varchar(500) not null,
        `created_at` real not null,
        unique key `idx_email` (`email`),
        key `idx_created_at` (`created_at`),
        primary key (`id`)
    ) engine=innodb default charset=utf8;
    
    create table blogs (
        `id` varchar(50) not null,
        `user_id` varchar(50) not null,
        `user_name` varchar(50) not null,
        `user_image` varchar(500) not null,
        `name` varchar(50) not null,
        `summary` varchar(200) not null,
        `content` mediumtext not null,
        `created_at` real not null,
        key `idx_created_at` (`created_at`),
        primary key (`id`)
    ) engine=innodb default charset=utf8;
    
    create table comments (
        `id` varchar(50) not null,
        `blog_id` varchar(50) not null,
        `user_id` varchar(50) not null,
        `user_name` varchar(50) not null,
        `user_image` varchar(500) not null,
        `content` mediumtext not null,
        `created_at` real not null,
        key `idx_created_at` (`created_at`),
        primary key (`id`)
    ) engine=innodb default charset=utf8;
    
四、编写配置文件(config.py)

为数据库的用户名、口令等编写一个配置文件，方便web App在不同环境获取正确的配置文件。

    config.py --基本配置文件
    config_default.py --开发环境配置文件
    config_override.py --生产环境配置文件

五、编写ORM--(orm.py)

5.1 创建连接池

    连接池由全局变量__pool存储，缺省情况下将编码设置为utf8，自动提交事务
    关于ORM详细介绍参考：http://www.luameows.wang/2018/03/09/%E5%88%9B%E7%AB%8BORM-%E5%BB%96%E9%9B%AA%E5%B3%B0python%E7%AC%94%E8%AE%B0/
    在获取连接池连接时，老版本使用__pool.get(),在新版本使用__pool.acqiure()
    关于全局变量的使用问题，可参考：https://docs.python.org/3/faq/programming.html#what-are-the-rules-for-local-and-global-variables-in-python
    conn.cursor(aiomysql.DictCursor):将结果作为字典返回的游标。所有方法和参数相同Cursor

创建select()和execute()函数

    select():SQL语句的点位符是?,而MySQL的点位符是%s,select()函数在内部自动替换.
    在一个协程中调用另一个协程并直接获得子协程的返回结果.
    如果传入size参数,通过fetchmany()获取最多指定数量的记录,否则,通过fetchall()获取所有记录
    execute():INSERT、UPDATE、DELETE这3种SQL执行都需要相同的参数以及返回一个整数表示影响的行数

5.2 创建ORM

    比如定义一个User对象，然后把数据表users和它关联起来。
    在User类中的__table__,id和name是类属性,不是实例的属性.
    在类级别上定义的属性用来描述User对象和表的映射关系,而实例属性必须通过__init__()方法去初始化.
    两者互不干扰.

5.3 定义Model

    要定义的是所有ORM映射的基类Model
    Model从dict继承,具备所有dict的功能,又要实现__getattr__()和__setattr__()两个特殊方法,
    因此又可以像引用普通字段那样写.
    
    定义Field和各种Field子类,映射varchar的StringField
    通过ModelMetaclass类将具体的子类如User的映射信息读取出来.
    
六. 创建数据模型(models.py)

    在Model里创建user,blog，comment三张表的模型类。
    
    
七. JSON API 定义(apis.py)
    
    JSON API错误类型定义


八. 创建GET、POST、ROUTE类(coroweb.py)

    1.定义GET方法
    2.定义POST方法
    3.定义ROUTE方法
    
九. 创建web框架(app.py)
    
    1.先创建一个简单的web主服务，验证启动起来(app1.py)
    2.web框架app.py
    
十. 创建MVC(handlers.py)

    1.在handlers中加入url请求地址，也就是控制层
    2.在templates目录中创建test.html，也就是展现层。

十一. 构建前端

    static/
    +--css/
    |  +--addons/
    |  |  +--uikit.addons.min.css
    |  |  +--uikit.almost-flat.addons.min.css
    |  |  +--uikit.gradient.addons.min.css
    |  +--awesome.css
    |  +--uikit.almost-flat.addons.min.css
    |  +--uikit.gradient.addons.min.css
    |  +--uikit.min.css 
    +--fonts/
    |  +--fontawesome-webfont.eot
    |  +--fontawesome-webfont.ttf
    |  +--fontawesome-webfont.woff
    |  +--FontAwesome.otf
    +--img
    |  +--user.png
    +--js/
    |  +--awesome.js
    |  +--html5.js
    |  +--jquery.min.js
    |  +--uikit.min.js
    |  +--sha1.min.js
    |  +--sticky.min.js
    |  +--vue.min.js
    +--README
    
    
    继承模板：{% extends 'base.html' %}
    子页面定义：{% block meta %}...{% endblock %}
    覆盖页面的标题:{% block title %}...{% endblock %}
    子页面在<head>标签关闭前插入javascript代码
    {% block beforehead %}...{% endblock %}
    子页面的content布局和内容
    {% block content %}
    ...
    {% endblock %}

11.1 构建基本模板

    基本模板：__base__.html
    
    日志模板：blogs.html

12. 编写API
    
    
    在handlers.py
    增加以下：
    @get('/api/users')
        async def api_get_users():
        users = await User.findAll(orderBy='created_at desc')
        return dict(users=users)
    在浏览器输入：
    http://127.0.0.1:9000/api/users
    
13. 注册与登录

13.1 注册并设置cookie
    
    增加注册模板:register.html
    在handlers.py增加注册请求：
    1).@get('/register')
       def register():
    2).@post('/api/users')
       async def api_register_user
    3).def user2cookie(user, max_age):
    
13.2 登录并设置cookie

    增加登录模板：signin.html
    在handlers.py增加登录请求：
    1).@get('/signin')
       def signin():
    2).@post('/api/authenticate')
       async def authenticate(*, email, passwd):
    3).def user2cookie(user, max_age):
    
13.3 用户退出并取消cookie
    
    修改基础模板用户状态信息(__base__.html)
    1).解析cookie在handlers.py
    async cookie2user(cookie_str)
    2).把登录用户绑定在request对象上写在app.py
    1>.async def auth_factory(app, handler)
    2>.app = web.Application(loop=loop, middlewares=[logger_factory, response_factory, auth_factory])
    3>.在def response_factory(app, handler):方法判断r是否dict实例else加入
     r['__user__'] = request.__user__