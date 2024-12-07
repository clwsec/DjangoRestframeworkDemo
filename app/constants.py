
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
        'default': 'default',
    }
