from src.admin_views import SecureModelView

class BookView(SecureModelView):
    
    column_searchable_list = ["title", "author"]