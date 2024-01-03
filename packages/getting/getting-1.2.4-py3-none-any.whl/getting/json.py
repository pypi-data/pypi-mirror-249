import copy


def recursive_process(data, data_processor, children_key, result_data=None):
    "递归处理函数，接受数据、数据处理函数和结果数据，以及子级数据（可选）"
    if result_data is None:
        result_data = []
    for item in data:
        new_item = copy.deepcopy(item)
        data_processor(new_item)
        if children_key in new_item:
            new_item[children_key] = recursive_process(
                new_item[children_key], data_processor, children_key=children_key
            )
        result_data.append(new_item)
    return result_data


def common_data_processor(item, operations):
    "通用的数据处理函数"
    for operation in operations:
        if operation["type"] == "remove_keys":
            keys_to_remove = operation["keys"]
            for key in keys_to_remove:
                item.pop(key, None)
        elif operation["type"] == "rename_key":
            old_key = operation["old_key"]
            new_key = operation["new_key"]
            if old_key in item:
                item[new_key] = item.pop(old_key)
        elif operation["type"] == "modify_value":
            key = operation["key"]
            value_modifier = operation["value_modifier"]
            if key in item:
                new_value = value_modifier(item[key])
                if new_value is not None:
                    item[key] = new_value


def execute_recursive_processing(json_list, operations, children_key):
    "执行递归处理并返回处理后的数据"
    processed_data = recursive_process(
        json_list, lambda item: common_data_processor(item, operations), children_key
    )
    return processed_data
