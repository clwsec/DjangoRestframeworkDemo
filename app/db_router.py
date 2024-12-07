from app.constants import AppConfigInfo

# TODO: 删除冗余日志 + 确认migrate是否正常(default数据库)
class RegionRouter:
    def db_for_read(self, model, **hints):
        print("**************model: ", model)
        if model._meta.db_table.startswith('goods_'):
            print("**************model._meta.db_table: ", model._meta.db_table)
            region = model._meta.db_table.split('_')[1]
            return f'{region}_db'
        return 'default'

    def db_for_write(self, model, **hints):
        print("@@@@@@@@@@@@@@@@@model: ", model)
        if model._meta.db_table.startswith('goods_'):
            region = model._meta.db_table.split('_')[1]
            return f'{region}_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = hints.get('instance', obj1)._state.db
        db_obj2 = hints.get('instance', obj2)._state.db
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print("**************model_name: ", model_name)
        print("**************app_label: ", app_label)
        print("**************db: ", db)
        print("**************hints: ", hints)
        model_name_str = str(model_name).lower()
        if model_name_str.endswith('good'):
            target_db = AppConfigInfo.DynamicModelMapDb.get(model_name_str)
            if target_db:
                return db == target_db
            return False
        return db == 'default'
