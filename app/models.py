from django.db import models

import uuid

# Create your models here.

class Notice(models.Model):
    
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # 使用UUID作为主键，默认值为自动生成的UUID，且不可编辑
    
    text = models.CharField( "内容", max_length=50 )      # verbose_name="内容" 定义了在数据表中显示的名称

    time = models.DateTimeField( "更新时间", auto_now=True)       # auto_now=True表示每次保存时自动更新为当前时间

    flag = models.BooleanField(default=False, verbose_name="是否完成" )        # default=False为默认的值
    
    user = models.ForeignKey(to='LoginData', on_delete=models.CASCADE, verbose_name="用户")  # ForeignKey表示一对多关系，on_delete=models.CASCADE表示级联删除
    
    class Meta:
        db_table = 'notice_data'
    
class LoginData(models.Model):

    username = models.CharField(max_length=30, unique=True, verbose_name="用户名")
    
    password = models.CharField(max_length=128, verbose_name="密码")
    
    email = models.EmailField(unique=True, verbose_name="邮箱")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    token = models.CharField(max_length=255, blank=True, null=True, verbose_name="令牌")
    
    class Meta:
        db_table = 'login_data'
        
# class LoginData(models.Model):
    
#     username = models.CharField(max_length=30, unique = True, verbose_name="用户名")
    
#     password = models.CharField(max_length=128,verbose_name="密码")
    
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
#     class meta:
#         db_table = 'login_data'
    
        
        
        
class EmailCode(models.Model):
    
    username = models.CharField(max_length=30, verbose_name="用户名")
    
    email = models.EmailField(unique=True, verbose_name="邮箱")
    
    code = models.CharField(max_length=6, verbose_name="验证码")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    
    class Meta:
        db_table = 'email_code'
    
