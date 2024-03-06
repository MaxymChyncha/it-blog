from django.core.paginator import Paginator


def paginate_context(request, queryset, context, count):
    paginator = Paginator(queryset, count)
    page_number = request.GET.get('page')
    paginated_object = paginator.get_page(page_number)
    context["paginated_obj"] = paginated_object
    context["paginator"] = paginated_object.paginator
    context["page_obj"] = paginated_object
    context["is_paginated"] = paginated_object.has_other_pages()
    return context
