def query(cursor, sql, params=None, is_execute=False):
    "pymysql 查询"
    # 执行查询
    if params is not None:
        execute = cursor.execute(sql, params)
    else:
        execute = cursor.execute(sql)
    # 获取查询结果
    results = None
    if is_execute is False:
        results = results_json(cursor)

    return execute, results


def insert(cursor, sql, params=None, is_execute=True):
    "pymysql 插入 最终需要 connection.commit() 提交更改"
    # 执行插入
    if params is not None:
        execute = cursor.execute(sql, params)
    else:
        execute = cursor.execute(sql)
    # 获取查询结果
    results = None
    if is_execute is False:
        results = results_json(cursor)
    return execute, results


def update(cursor, sql, params=None, is_execute=True):
    "pymysql 更新 最终需要 connection.commit() 提交更改"
    # 执行更新
    if params is not None:
        execute = cursor.execute(sql, params)
    else:
        execute = cursor.execute(sql)
    # 获取查询结果
    results = None
    if is_execute is False:
        results = results_json(cursor)
    return execute, results


def results_json(cursor):
    "查询结果并json化"
    results = cursor.fetchall()
    # 获取字段名
    column_names = [desc[0] for desc in cursor.description]
    # 构建字典列表，每个字典表示一行数据
    results = [dict(zip(column_names, row)) for row in results]
    return results
