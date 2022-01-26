from dfwtaichi.styles.models import Style


def style_menu(request):
    style_menu = {"style_menu": Style.objects.values("title", "slug")}
    return style_menu
