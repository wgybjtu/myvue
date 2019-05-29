一、WEB后端构建

1、创建Django工程，可用pycharm直接创建，或者使用命令

      工程名为myvue (创建命令：django-admin startproject）

2、创建自己的APP

       python manage.py startapp myapp

3、在myvue/myvue/setting.py 下面将myapp 添加至

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp', #添加自己的app
]
   

4、myapp目录下的models.py里我们简单写一个model如下：

# coding:utf-8
from __future__ import unicode_literals
from django.db import models

class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name
5、在myapp目录下的views里我们新增两个接口，一个是show_books返回所有的书籍列表（通过JsonResponse返回能被前端识别的json格式数据），二是add_book接受一个get请求，往数据库里添加一条book数据：

# coding:utf-8
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
import json
from myapp.models import Book


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except :
        response['msg'] = '添加错误'
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except :
        response['msg'] = '获取错误'
        response['error_num'] = 1

    return JsonResponse(response)

6、在myapp目录下，新增一个urls.py文件，把我们新增的两个接口添加到路由里：

# coding:utf-8
__author__ = 'jing'
__date__ = '2019-05-29 13:57'
from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
]
7、在主目录myvue/myvue/url.py下的urls添加到project下的urls中，才能完成路由：

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
import myapp.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('^api/', include(myapp.urls)),
    path('', TemplateView.as_view(template_name="index.html")),
]
8、在项目的主目录myvue/，输入命令：

python manage.py makemigrations myapp

python manage.py migrate

查询数据库，看到book表已经自动创建了：

9、项目启动

    python manage.py runserver

10、后端测试

   http://127.0.0.1:8000/api/add_book?book_name='钢铁是怎样炼成的‘

     http://127.0.0.1:8000/api/show_books

二、VUE前端构建

1、先用npm安装vue-cli脚手架工具（vue-cli是官方脚手架工具，能迅速帮你搭建起vue项目的框架）：

`npm install -g vue-cli`
2、安装好后，在project项目根目录下，新建一个前端工程目录：


vue init webpack appfront  //安装中把vue-router选上，我们须要它来做前端路由
3、进入appfront目录，运行命令：

    npm install //安装vue所须要的node依赖

4、appfront/src/main.js
 

import Vue from 'vue'
import App from './App'
import router from './router'

import VueResource from 'vue-resource'

Vue.config.productionTip = false

Vue.use(VueResource)


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
5、appfront/src/components/Home.vue
 

<template>
  <div class="home">
    <el-row display="margin-top:10px">
        <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
        <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
        <el-table :data="bookList" style="width: 100%" border>
          <el-table-column prop="id" label="编号" min-width="100">
            <template scope="scope"> {{ scope.row.pk }} </template>
          </el-table-column>
          <el-table-column prop="book_name" label="书名" min-width="100">
            <template scope="scope"> {{ scope.row.fields.book_name }} </template>
          </el-table-column>
          <el-table-column prop="add_time" label="添加时间" min-width="100">
            <template scope="scope"> {{ scope.row.fields.add_time }} </template>
          </el-table-column>
        </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: '',
      bookList: [],
    }
  },
  mounted: function() {
      this.showBooks()
  },
  methods: {
    addBook(){
      this.$http.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.showBooks()
            } else {
              this.$message.error('新增书籍失败，请重试')
              console.log(res['msg'])
            }
        })
    },
    showBooks(){
      this.$http.get('http://127.0.0.1:8000/api/show_books')
        .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (res.error_num == 0) {
              this.bookList = res['list']
            } else {
              this.$message.error('查询书籍失败')
              console.log(res['msg'])
            }
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
6、在src/router目录的index.js中，我们把新建的Home组件，配置到vue-router路由中：

import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/Home'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Home',
      component: Home
    }
  ]
})
7、按照并启动vue
 

    npm install --save vue-resource  

    npm run dev

三、Vue 引入elementUI

1、npm install -g webpack

2、安装load模块

    npm install style-loader -D
    npm install css-loader -D
    npm install file-loader -D2 安装 Element-UI 模块
    npm install element-ui --save
3、 修改 myvue/appfront/build/webpack.base.conf.js

{
    test: /\\\\\\\\.css$/,
    loader: "style!css"
},
{
    test: /\\\\\\\\.(eot|woff|woff2|ttf)([\\\\\\\\?]?.*)$/,
    loader: "file"
}
4、修改myvue/appfront/src/main.js

   打开项目：src/main.js,添加下面三条      
   import ElementUI from 'element-ui'
   import 'element-ui/lib/theme-chalk/index.css'
   Vue.use(ElementUI)
四、其他问题
 

1、如果发现列表抓取不到数据，可能是出现了跨域问题，打开浏览器console确认：


 


2、这时候我们须要在Django层注入header，用Django的第三方包django-cors-headers来解决跨域问题：

       pip install django-cors-headers
3、settings.py 修改：

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
CORS_ORIGIN_ALLOW_ALL = True
  注意中间件的添加顺序
4、在前端工程目录下，输入npm run build，如果项目没有错误的话，就能够看到所有的组件、css、图片等都被webpack自动打包到dist目录下了


五、 整合Django和Vue.js
1、目前我们已经分别完成了Django后端和Vue.js前端工程的创建和编写，但实际上它们是运行在各自的服务器上，和我们的要求是不一致的。因此我们须要把Django的TemplateView指向我们刚才生成的前端dist文件即可。

2、需要配置一下模板使Django知道从哪里找到index.html。在project目录的settings.py下


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), 'appfront/dist']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
3、我们还需要配置一下静态文件的搜索路径。同样是project目录的settings.py下：


# Add for vuejs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "appfront/dist/static"),]
4、配置完成，我们在project目录下输入命令python manage.py runserver，就能够看到我们的前端页面在浏览器上
 

Screen Shot 2019-05-29 at 14.53.06.png 六、服务器部署

环境搭建与部署

登录主机，用你刚填写的密码：

ssh root@ IP
CentOS 系统可以使用 yum 安装必要的包

# 如果你使用git来托管代码的话
yum install git

# 如果你要在服务器上构建前端
yum install nodejs
yum install npm

yum install nginx
我们使用 uwsgi 来处理 Django 请求，使用 nginx 处理 static 文件（即之前 build 之后 dist 里面的static，这里默认前端已经打包好了，如果在服务端打包前端需要安装nodejs，npm等）
安装uWsgi

yum install uwsgi
# 或者
pip install uwsgi
我们使用配置文件启动uwsgi，比较清楚

uwsgi配置文件：

[uwsgi]
socket = 127.0.0.1:9292
stats = 127.0.0.1:9293
workers = 4
# 项目根目录
chdir = /opt/inner_ulb_manager
touch-reload = /opt/inner_ulb_manager
py-auto-reload = 1
# 在项目跟目录和项目同名的文件夹里面的一个文件
module= inner_ulb_manager.wsgi
pidfile = /var/run/inner_ulb_manager.pid
daemonize = /var/log/inner_ulb_manager.log
nginx 配置文件：

server {
    listen 8888;
    server_name you ip;
    root /opt/inner_ulb_manager;
    access_log /var/log/nginx/access_narwhals.log;
    error_log /var/log/nginx/error_narwhals.log;

    location / {
            uwsgi_pass 127.0.0.1:9292;
            include /etc/nginx/uwsgi_params;
    }
    location /static/ {
            root  /opt/inner_ulb_manager/;
            access_log off;
    }
    location ^~ /admin/ {
            uwsgi_pass 127.0.0.1:9292;
            include /etc/nginx/uwsgi_params;
    }
}
/opt/inner_ulb_manager/static 即为静态文件目录，那么现在我们静态文件还在 frontend/dist 怎么办，不怕，Django给我们提供了命令：

先去settings里面配置：

STATIC_ROOT = os.path.join(BASE_DIR, "static")
然后在存在manage.py的目录，即项目跟目录执行：

python manage.py collectstatic
这样frontend/dist/static里面的东西就到了项目根目录的static文件夹里面了

那么为什么不直接手动把构建好的dist/static拷过来呢，因为开始提过Django自带的App：admin 也有一些静态文件（css,js等），它会一并collect过来，毕竟nginx只认项目跟目录的静态文件，它不知道django把它自己的需求文件放到哪了

开头说过Django配置灵活，那么我们专门为Django创建一个生产环境的配置 prod.py

prod.py 与 默认 settings.py 同目录

# 导入公共配置
from .settings import *

# 生产环境关闭DEBUG模式
DEBUG = False

# 生产环境开启跨域
CORS_ORIGIN_ALLOW_ALL = False

# 特别说明，下面这个不需要，因为前端是VueJS构建的，它默认使用static作为静态文件入口，我们nginx配置static为入口即可，保持一致，没Django什么事
STATIC_URL = '/static/'

如何使用这个配置呢，进入 wisg.py 即uwsgi配置里面的module配置修改为：

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "**inner_ulb_manager.prod**")

application = get_wsgi_application()
启动uwsgi

uwsgi --ini inner_ulb_manager.ini


启动ngingx

service nginx start
至此，部署就完成了

文章学习源：

https://zhuanlan.zhihu.com/p/24893786

https://cloud.tencent.com/developer/article/1005607

https://segmentfault.com/a/1190000011023102