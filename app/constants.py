
class AppConfigInfo:
    # 地区
    REGIONS = [
        ('south', '南方'),
        ('north', '北方'),
        ('east', '东方'),
        ('west', '西方'),
        ('central', '中部'),
    ]
    # 动态模型映射数据库
    DynamicModelMapDb = {
        'southgood': 'south_db',
        'northgood': 'north_db',
        'eastgood': 'east_db',
        'westgood': 'west_db',
        'centralgood': 'central_db',
        'default': 'default', # 配置了，但是因为db_router的allow_migrate逻辑，所以不会在default数据库中生成相关的Good表
    }
