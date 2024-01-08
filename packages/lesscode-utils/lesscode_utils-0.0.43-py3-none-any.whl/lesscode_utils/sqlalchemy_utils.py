def condition_by_between(filters: list, model, column, start_value, end_value):
    _filter = None
    if start_value is not None and end_value is not None:
        _filter = getattr(model, column).between(start_value, end_value)
        filters.append(_filter)
    return _filter


def condition_by_in(filters: list, model, column, value):
    _filter = None
    if value and isinstance(value, list):
        _filter = getattr(model, column).in_(value)
        filters.append(_filter)
    return _filter


def condition_by_like(filters: list, model, column, value, position: str = "LR"):
    _filter = None
    if value:
        if position == "LR":
            value = f"%{value}%"
        elif position == "L":
            value = f"%{value}"
        elif position == "R":
            value = f"{value}%"
        else:
            value = f"%{value}%"
        _filter = getattr(model, column).like(value)
        filters.append(_filter)
    return _filter


def condition_by_not_in(filters: list, model, column, value):
    _filter = None
    if value is not None:
        _filter = getattr(model, column).notin_(value)
        filters.append(_filter)
    return _filter


def condition_by_not_like(filters: list, model, column, value):
    _filter = None
    if value:
        _filter = getattr(model, column).notlike(value)
        filters.append(_filter)
    return _filter


def condition_by_is_null(filters: list, model, column):
    _filter = getattr(model, column).is_(None)
    filters.append(_filter)
    return _filter


def condition_by_not_null(filters: list, model, column):
    _filter = getattr(model, column).isnot(None)
    filters.append(_filter)
    return _filter


def condition_by_not_in_list(filters: list, model, column, value):
    _filter = None
    if value is not None:
        _filter = ~getattr(model, column).in_(value)
        filters.append(_filter)
    return _filter


def condition_by_eq(filters: list, model, column, value):
    _filter = None
    if value:
        _filter = getattr(model, column) == value
        filters.append(_filter)
    return _filter


def query_with_order_by(query, order_by_list: list = None):
    """
    :param query:
    :param order_by_list: [{"column":User.id,"order":"desc"}]
    :return:
    """
    if order_by_list is not None:
        for order in order_by_list:
            column = order.get("column")
            if column:
                if order.get("order") == "desc":
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column.asc())
    return query


def single_model_format_order(model, sort_list):
    """
    :param model:
    :param sort_list: [{"column":"id","order":"desc"}]
    :return:
    """
    new_sort_list = []
    if sort_list is not None:
        for order in sort_list:
            column = order.get("column")
            if column:
                if hasattr(model, column):
                    column = getattr(model, column)
                    if order.get("order") == "desc":
                        column = column.desc()
                    else:
                        column = column.asc()
                    new_sort_list.append(column)
    return new_sort_list
