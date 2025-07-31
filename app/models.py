from django.db import models

# Create your models here.

class Notice(models.Model):
    
    text = models.CharField( "text", max_length=50 )      # verbose_name="内容" 定义了在数据表中显示的名称

    # time = models.DateTimeField( "time", auto_now=True)       # auto_now=True表示每次保存时自动更新为当前时间

    # flag = models.BooleanField( "flag", default=False, verbose_name="是否完成" )        # default=False为默认的值
    