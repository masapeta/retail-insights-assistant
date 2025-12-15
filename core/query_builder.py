def build_sql(intent: dict, metric: str = None):

    filters = intent.get("filters", {})
    group_by = intent.get("group_by", [])

    where_clauses = []
    for col, value in filters.items():
        if isinstance(value, (int, float)) or str(value).replace(".", "", 1).isdigit():
            where_clauses.append(f"{col} = {value}")
        else:
            where_clauses.append(f"{col} = '{value}'")

    where = ""
    if where_clauses:
        where = " WHERE " + " AND ".join(where_clauses)

    if metric is None:
        select_clause = (
            ", ".join(group_by) + ", COUNT(*) AS row_count" 
            if group_by else 
            "COUNT(*) AS row_count"
        )

        sql = f"SELECT {select_clause} FROM sales_data{where}"
        if group_by:
            sql += " GROUP BY " + ", ".join(group_by)
        sql += " ORDER BY row_count DESC"
        return sql

    select_clause = (
        ", ".join(group_by) + f", SUM({metric}) AS total_{metric}"
        if group_by else
        f"SUM({metric}) AS total_{metric}"
    )

    sql = f"SELECT {select_clause} FROM sales_data{where}"

    if group_by:
        sql += " GROUP BY " + ", ".join(group_by)

    sql += f" ORDER BY total_{metric} DESC"

    return sql
