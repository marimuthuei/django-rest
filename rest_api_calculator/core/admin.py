from django.contrib import admin
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import User, Group


class CustomAdmin(admin.AdminSite):
    site_title = ugettext_lazy('API admin')

    site_header = ugettext_lazy('Admin Console')

    index_title = ugettext_lazy('Site administration')


admin_site = CustomAdmin()
admin_site.register(User)
admin_site.register(Group)
