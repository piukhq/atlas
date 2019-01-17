from django.contrib import admin

from ubiquity_users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['email', 'opt_out_timestamp', 'time_added_to_database']
