from django.db import models
# Create your models here.

class LessonTable(models.Model):
    
    week = models.IntegerField( verbose_name="第几周" )
    
    day = models.CharField( max_length=3, verbose_name="星期几" )  # 例如：Mon, Tue, Wed, Thu, Fri, Sat, Sun
    
    lesson = models.CharField( max_length=50, verbose_name="课程" )  # 课程名称
    
    start_time = models.TimeField( verbose_name="开始时间" )  # 例如：08:00, 09:30, 14:00
    
    day_time = models.IntegerField( verbose_name="上午/下午/晚上") # 1表示上午，2表示下午，3表示晚上 
    
    startime = models.DateField( verbose_name="学期开始时间" )      # models.DateField这个字段在插入时可以用Semester.objects.create(startime=datetime.date(2025, 8, 8))
    creatime = models.DateTimeField( auto_now_add=True, verbose_name="创建时间" )   # auto_now_add=True表示在对象第一次创建时设置为当前时间，以后不会再更新
    location = models.CharField( max_length=50, verbose_name="教室位置")
    teacher = models.CharField(max_length=20, verbose_name="教师名字")

    user = models.ForeignKey(to='app.LoginData', on_delete=models.CASCADE, verbose_name="用户")  # ForeignKey表示一对多关系，on_delete=models.CASCADE表示级联删除
    
    class Meta:
        db_table = 'lessonTable'