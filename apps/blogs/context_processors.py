from .models import CategoriesModel, TagsModel, BlogsModel

def sidebar_data(request):
    return {
        "categories": CategoriesModel.objects.all(),
        "tags": TagsModel.objects.all(),
        "recent_blogs": BlogsModel.objects.order_by("-created_at")[:2],
    }
