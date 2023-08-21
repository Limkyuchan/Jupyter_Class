from django.contrib import admin
from .models import UploadFile, ImgModel

# Register your models here.

admin.site.register(UploadFile)
admin.site.register(ImgModel)