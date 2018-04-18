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
查看已安装的第三方库

    conda list

