from django.db import models
from django_base64field.fields import Base64Field

# Create your models here.

class UploadFile(models.Model):
    file = models.FileField()
    
    def __str__(self):
        return f"upload_file : {self.file}"
    

class ImgModel(models.Model):
    # 운동 기구 이미지 파일
    img_data = Base64Field(max_length=900000, blank=True, null=True)
    
    # 운동 클래스 번호
    ex_class = models.IntegerField()
    
    # 운동 기구 이름
    ex_name = models.CharField(max_length=50)
    
    # 예측 퍼센트
    ex_per = models.FloatField(null=True)
    
    def __str__(self):
        return f"file_name : {self.img_data}"
    

class Exercise(models.Model):
    
    ex_name = models.CharField(max_length=100, blank=True)
    ex_part = models.CharField(max_length=50, blank=True)
    ex_method = models.TextField()
    ex_video1 = models.TextField()
    ex_video2 = models.TextField()
    
    def __str__(self):
        return f"name:{self.ex_name}, part:{self.ex_part}, method:{self.ex_method}, video1:{self.ex_video1}, video2:{self.ex_video2}"