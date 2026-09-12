from django.contrib import admin

from .models import Member

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_filter = ("address","full_name","status", "joined_date")
    list_display = ("id","full_name","phone", "joined_date") 
    search_fields = (
        "full_name",
        "phone",
        "email",

    )


admin.site.register(Member,MemberAdmin)

