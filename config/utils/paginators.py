from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest


def paginate_context(
        request: HttpRequest,
        queryset: QuerySet,
        context: dict,
        count: int
):
    paginator = Paginator(queryset, count)
    page_number = request.GET.get('page')
    paginated_object = paginator.get_page(page_number)
    context["paginated_obj"] = paginated_object
    context["paginator"] = paginated_object.paginator
    context["page_obj"] = paginated_object
    context["is_paginated"] = paginated_object.has_other_pages()
    return context
