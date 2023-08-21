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
    ex_class = models.IntegerField(max_length=10)
    
    # 운동 기구 이름
    ex_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"file_name : {self.img_data}"