from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from django.contrib.auth import get_user_model

from main.models import Content, Channel
from main.forms import UserChangeForm,UserCreationForm, SuperuserAuthenticationForm, ChannelAdminForm
from django_summernote.admin import SummernoteModelAdmin
from django_admin_bootstrapped.widgets import GenericContentTypeSelect

User = get_user_model()

class AdminRootSite(AdminSite):
    site_header = '라됴 관리자 페이지'
    login_form = SuperuserAuthenticationForm

    def has_permission(self, request):
        # superuser 권한이 없을 경우 login 페이지로 무조건 리-다이렉트 된다.
        return request.user.is_active and request.user.is_superuser

admin_root = AdminRootSite(name='admin')

@admin.register(User, site=admin_root)
class UserAdmin(DefaultUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'nickname', 'date_joined', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nickname',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser','groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(Channel, site=admin_root)
class ChannelAdmin(admin.ModelAdmin):

    list_display = ['bg_preview', 'ch_name', 'user', 'created']
    fieldsets = (
        (None,  {'fields': ('ch_name', 'user', 'bg_img', 'brief', 'intro')}),
    )

    # formfield_overrides = {
    #     'user': {'widget': GenericContentTypeSelect},
    # }

    def bg_preview(self, obj):
        if obj.bg_img:
            return '<img src="%s" style="height: 50px; width: auto">' % (obj.bg_img.url)
        else:
            "no image"

    # def uploaded_bg_preview(self):
    #     return '<img src="/media/%s" width="100" height="100" />' % (self.photo)
    #         image_thumb.allow_tags = True
    #
    #
    bg_preview.allow_tags = True
    bg_preview.short_description = "배경화면"



@admin.register(Content, site=admin_root)
class ContentAdmin(SummernoteModelAdmin):
    form = ChannelAdminForm
    list_display = ['thumb_preview', 'channel', 'title', 'created', 'updated']

    fieldsets = (
        (None,  {'fields': ('channel', 'title', 'thumb_img', 'body', )}),
    )


    def thumb_preview(self, obj):
        if obj.thumb_img:
            return '<img src="%s" style="height: 50px; width: auto">' % (obj.thumb_img.url)
        else:
            "no image"

    thumb_preview.allow_tags = True
    thumb_preview.short_description = "썸네일 이미지"


from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from allauth.socialaccount.admin import SocialAppAdmin, SocialTokenAdmin, SocialAccountAdmin
from django.contrib.sites.models import Site
from django.contrib.sites.admin import SiteAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

admin_root.register(SocialApp, SocialAppAdmin)
admin_root.register(SocialToken, SocialTokenAdmin)
admin_root.register(SocialAccount, SocialAccountAdmin)
admin_root.register(Site, SiteAdmin)
admin_root.register(Group, GroupAdmin)

