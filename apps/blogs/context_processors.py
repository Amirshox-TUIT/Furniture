from .models import CategoriesModel, TagsModel, BlogsModel


def sidebar_data(request):
    categories = CategoriesModel.objects.filter(sub__isnull=True)
    return {
        "categories": categories,
        "tags": TagsModel.objects.all(),
        "recent_blogs": BlogsModel.objects.order_by("-created_at")[:2],
    }
