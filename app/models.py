from django.db import models
from app.constants import AppConfigInfo

# 单数据库，多表实现


class Post(models.Model):

    title = models.CharField(
        max_length=200,
        verbose_name='标题',
        db_index=True,  # 设置索引
        unique=True
    )
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True
        # unique_together = ('title', 'created_at')  # 多字段唯一约束


# 动态创建模型类
def create_region_post_model(region):
    class Meta:
        db_table = f'posts_{region}'

    attrs = {
        '__module__': Post.__module__,
        'Meta': Meta,
    }
    print("##################：", attrs)
    return type(f'{region.capitalize()}Post', (Post,), attrs)


# 创建所有地区的模型
region_models = {region: create_region_post_model(region) for region, _ in AppConfigInfo.REGIONS}


def get_post_model(region):
    return region_models.get(region)
