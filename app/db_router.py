from app.constants import AppConfigInfo

# 多数据库场景使用
class RegionRouter:
    def db_for_read(self, model, **hints):
        """
        model: 当执行查询操作时传入的模型类（不是实例）
        hints: 额外的提示信息字典
        调用时机：当执行任何读取操作（如 Model.objects.get(), filter() 等）时自动调用
        """
        print("db_for_read model: ", model)
        if model._meta.db_table.startswith('goods_'):
            print("db_for_read model._meta.db_table: ", model._meta.db_table)
            region = model._meta.db_table.split('_')[1]
            return f'{region}_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        model: 当执行写入操作时传入的模型类（不是实例）
        hints: 额外的提示信息字典
        调用时机：当执行任何写入操作（如 Model.objects.create(), update(), delete() 等）时自动调用
        """
        print("db_for_write model: ", model)
        if model._meta.db_table.startswith('goods_'):
            region = model._meta.db_table.split('_')[1]
            return f'{region}_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        用于控制两个模型对象之间是否允许建立关系（比如外键关系）。
        使用场景：
            这个方法主要用于多数据库架构中
            通常的做法是只允许同一数据库中的对象建立关系
            这可以防止跨数据库的外键关系，这种关系可能会导致数据一致性问题
        参数：
        obj1, obj2: 要建立关系的两个模型实例
        hints: 包含额外信息的字典，其中可能包含 'instance' 键
        调用时机：创建外键关系时
            使用 select_related() 进行关联查询时
            保存带有外键关系的对象时
        下面的代码中，这个实现确保了只有在同一个数据库中的对象才能建立关系，这是一个比较安全和常见的实践。
        """
        db_obj1 = hints.get('instance', obj1)._state.db
        db_obj2 = hints.get('instance', obj2)._state.db
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        用于控制是否在特定的数据库中迁移模型。
        使用场景：
            这个方法主要用于多数据库架构中，
            通常的做法是只允许在特定的数据库中迁移模型，
            这可以防止模型在错误的数据库中迁移，导致数据不一致。
        db: 当前正在考虑进行迁移的数据库别名（如 'default', 'east_db'）
        app_label: Django 应用的名称
        model_name: 要迁移的模型名称
        hints: 额外的迁移提示信息
        调用时机：
            执行 python manage.py migrate 命令时
            执行 python manage.py migrate --database=east_db 等特定数据库迁移命令时
        migrate的时候需要执行对应的db, 如: python manage.py migrate --database=east_db
        """
        print("allow_migrate db: ", db)
        print("allow_migrate app_label: ", app_label)
        print("allow_migrate model_name: ", model_name)
        print("allow_migrate hints: ", hints)
        model_name_str = str(model_name).lower()
        if model_name_str.endswith('good'):
            target_db = AppConfigInfo.DynamicModelMapDb.get(model_name_str)
            if target_db:
                return db == target_db
            return False
        return db == 'default'
