from .models import Exhibition


def create_exhibition(
    *,
    title,
    category,
    description,
    image="",
    start_date=None,
    end_date=None,
    is_permanent=False,
    is_active=True,
):
    exhibition = Exhibition.objects.create(
        title=title,
        category=category,
        description=description,
        image=image,
        start_date=start_date,
        end_date=end_date,
        is_permanent=is_permanent,
        is_active=is_active,
    )

    return exhibition
