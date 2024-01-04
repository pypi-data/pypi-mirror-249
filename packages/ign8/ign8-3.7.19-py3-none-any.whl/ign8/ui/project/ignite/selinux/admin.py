from django.contrib import admin
from .models import Selinux
from .models import SElinuxEvent


admin.site.register(Selinux)
admin.site.register(SElinuxEvent)


