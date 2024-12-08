from django.db import models
from app.constants import AppConfigInfo

# 多数据库实现，注意每个数据库要单独执行migrate才会生成对应的表


class Good(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def create_region_good_model(region):
    class Meta:
        db_table = f'goods_{region}'
        # app_label = 'app'

    attrs = {
        '__module__': Good.__module__,
        'Meta': Meta,
    }
    print("##################：", attrs)
    return type(f'{region.capitalize()}Good', (Good,), attrs)


# 创建所有地区的模型
region_good_models = {
    region: create_region_good_model(region) for region, _ in AppConfigInfo.REGIONS}


def get_good_model(region):
    return region_good_models.get(region)
