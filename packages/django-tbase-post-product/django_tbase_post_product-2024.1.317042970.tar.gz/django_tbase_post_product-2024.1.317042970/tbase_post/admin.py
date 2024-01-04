from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Post,AmazonSettings,PostSettings,Link
# from markdownx.admin import MarkdownxModelAdmin
# from markdownx.widgets import AdminMarkdownxWidget
from martor.widgets import AdminMartorWidget
from solo.admin import SingletonModelAdmin
from django.utils.safestring import mark_safe
from django.utils.safestring import SafeText

from hitcount.models import HitCount
from hitcount.views import HitCountMixin

def make_published(modeladmin, request, queryset):
    # 设为发布
    make_published.short_description = "批量设为发布"
    queryset.update(publish_status='published')
def make_draft(modeladmin, request, queryset):
    # 批量设为草稿
    make_draft.short_description = "批量设为草稿"
    queryset.update(publish_status='draft')

def make_trash(modeladmin, request, queryset):
    # 设为trash
    make_trash.short_description = "批量设为垃圾内容"
    queryset.update(publish_status='trash')




class LinkAdmin(admin.ModelAdmin):
## 链接，用于搜索优化，手动配置内链接
    save_on_top = True
    list_display = ('title','url','updated_on')
admin.site.register(Link, LinkAdmin)





class PostAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('title','image_data',
        'formatted_hit_count',
        'publish_status','updated_on','product_name','product_id','youtube_id')
    list_filter = (['updated_on','publish_status']) # 过滤字段
    search_fields =('title', 'product_name','product_id')  # 设置搜索字段
    ordering = ('-updated_on','product_name','product_id')
    # 设置批量处理
    actions = [make_published,make_draft,make_trash]
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMarkdownxWidget},
    # }
    fieldsets = (
          ('基本', {
                'fields': ['title']
            }),
            ('产品信息', {
                'fields': ('product_name', 'product_id', 'article_img','image_data',
                            'youtube_id','youtube_player','publish_status'
                            ),
            }),
            ('seo优化', {
                'fields': ('tags', 'meta_keywords', 'meta_description'),
            }),
            ('内容', {
                'fields': ['content'],
            }),
            ('资料', {
                'fields': ['data'],
            }),
        )

    readonly_fields=('image_data','youtube_player',)


    def formatted_hit_count(self, obj):
        # print(dir(obj))
        # print(obj.hit_count_generic())
        hit_count = HitCount.objects.get_for_object(obj)
        return hit_count.hits
    #     return obj.current_hit_count() if obj.current_hit_count() > 0 else '-'
    # formatted_hit_count.admin_order_field = 'hit_count'
    # formatted_hit_count.short_description = 'Hits'




    def image_data(self, obj):
        return mark_safe(f'<img width="100px" class="list_img_article_img" src="{obj.article_img}">')


    def youtube_player(self, obj):
        return SafeText(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{obj.youtube_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>')
 


 
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }








#
#    def make_published(self, request, queryset):
#        # 设为发布
#        queryset.update(publish_status='published')
#
#
#
#
#    def make_published(self, request, queryset):
#        # 设为发布
#        queryset.update(publish_status='published')
#






admin.site.register(Post, PostAdmin)

class AmazonSettingsAdmin(SingletonModelAdmin):
    # form = ConfigurationForm):
    # form = ConfigurationForm
    # list_display = ('site_title', 'maintenance_mode')
    # 编辑页面字段定制
    # fieldsets = [
    #     ("Base information", {
    #         'fields': [
    #             'store_id'
    #         ]
    #     }),
       
    # ]
    pass
# 注册配置页面
admin.site.register(AmazonSettings, AmazonSettingsAdmin)




class PostSettingsAdmin(SingletonModelAdmin):
    """
    Post 相关设置信息 后台管理页面
    
    """
    # form = ConfigurationForm):
    # form = ConfigurationForm
    # list_display = ('site_title', 'maintenance_mode')
    # 编辑页面字段定制
    # fieldsets = [
    #     ("Base information", {
    #         'fields': [
    #             'store_id'
    #         ]Post
    #     }),
       
    # ]
    pass
# 注册配置页面
admin.site.register(PostSettings, AmazonSettingsAdmin)






# class PostAdmin(MarkdownxModelAdmin):
#     list_display = ('title', 'created_on')
#     pass
# # admin.site.register(Post, PostAdmin)
# admin.site.register(Post, PostAdmin)
