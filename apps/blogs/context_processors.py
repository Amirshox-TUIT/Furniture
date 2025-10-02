from .models import CategoriesModel, TagsModel, BlogsModel


def sidebar_data(request):
    categories = CategoriesModel.objects.filter(sub__isnull=True)
    return {
        "categories": categories,
        "tags": TagsModel.objects.all(),
        "recent_blogs": BlogsModel.objects.order_by("-created_at")[:2],
    }


def social_medias(request):
    return {
        'twitter':'http://www.flow.amirshox.uz/accounts/profile/1',
        'telegram':'https://t.me/STARBOY_1505',
        'github':'https://github.com/Amirshox-TUIT',
        'linkedin':'https://www.linkedin.com/in/amir-ravik-4206662a8'
    }
