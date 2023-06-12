from django.urls import path, include
from acquisition import views

urlpatterns = [
    path('index/', views.index, name='index'), #首页
    path('allscan/', views.allscan, name="allscan"), #扫描列表
    path('dirresult/<int:sid>/', views.dirresult, name="dirresult"), #目录扫描
    path('portresult/<int:sid>/', views.portresult, name="portresult"), #端口扫描
    path('cmsresult/<int:sid>/', views.cmsresult, name="cmsresult"), #CMS扫描
    path('wafresult/<int:sid>/', views.wafresult, name="wafresult"), #whios
    path('httpsresult/<int:sid>/', views.httpsresult, name="httpsresult"), #https
    path('subresult/<int:sid>/', views.subresult, name="subresult"), #子域名
]