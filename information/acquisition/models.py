from django.db import models

# Create your models here.

class ScanList(models.Model):
    """ 目标 """
    name = models.CharField(max_length=32, verbose_name="用户名")
    url = models.TextField(max_length=200, blank=True, default='', verbose_name="目标地址")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "扫描列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class dirList(models.Model):
    """ 目录扫描列表 """
    sid = models.ForeignKey(to="ScanList", to_field="id", on_delete=models.CASCADE)
    url = models.TextField(max_length=200, blank=True, default='', verbose_name="目标地址")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    fileway = models.TextField(max_length=500, blank=True, default='', verbose_name="文件路径")

    class Meta:
        verbose_name = "目录扫描"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.url

class Port(models.Model):
    """ 端口扫描列表 """
    sid = models.ForeignKey(to="ScanList", to_field="id", on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    port = models.TextField(max_length=500, blank=True, default='', verbose_name="扫描端口")
    ip = models.TextField(max_length=200, blank=True, default='', verbose_name="IP地址")

    class Meta:
        verbose_name = "端口扫描"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sid

class Cmslist(models.Model):
    """ 指纹识别列表 """
    sid = models.ForeignKey(to="ScanList", to_field="id", on_delete=models.CASCADE)
    url = models.TextField(max_length=200, blank=True, default='', verbose_name="目标地址")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    cms = models.TextField(max_length=500, blank=True, default='', verbose_name="指纹")

    class Meta:
        verbose_name = "指纹识别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sid