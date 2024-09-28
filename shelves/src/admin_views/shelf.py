from src.admin_views import SecureModelView

class ShelfView(SecureModelView):
    
    column_searchable_list = ["shelf_name"]