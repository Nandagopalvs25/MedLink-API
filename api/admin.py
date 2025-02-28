from django.contrib import admin
from .models import CustomUser,Patient,Record,Post
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(Post)
