from django.db import models

# Create your models here.

class ChatTable(models.Model):
    question = models.CharField(max_length=50)
    
    answer = models.CharField(max_length=50)
    
    user = models.ForeignKey(to='app.LoginData', on_delete=models.CASCADE, verbose_name="用户")
    
    class Meta:
        db_table = "ChatTable"