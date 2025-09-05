from .models import CategoriesModel, TagsModel, BlogsModel
from ..products.models import ProductCategory


def sidebar_data(request):
    categories = ProductCategory.objects.filter(sub__isnull=True)
    return {
        "categories": categories,
        "tags": TagsModel.objects.all(),
        "recent_blogs": BlogsModel.objects.order_by("-created_at")[:2],
    }
