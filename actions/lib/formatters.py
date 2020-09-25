def format_client_list_result(result, exclude_attributes=None):
    """
    Format an API client list return which contains a list of objects.

    :param exclude_attributes: Optional list of attributes to exclude from the item.
    :type exclude_attributes: ``list``

    :rtype: ``list`` of ``dict``
    """
    formatted = []

    for item in result:
        value = item.to_dict(exclude_attributes=exclude_attributes)
        formatted.append(value)

    return formatted


def format_result(item):
    return item.to_dict() if item else None


def format_rule_update_result(result, exclude_attributes):
    return format_client_list_result(result=[result], exclude_attributes=exclude_attributes)[0]


def format_rule_result(rule, exclude):
    if rule is None or isinstance(rule, str):
        # error happened
        return False, rule
    else:
        # all good here
        return True, format_rule_update_result(rule, exclude)
