from typing import List
from typing import Optional

import records

import common


def get_ranking_of_user(name: str, record_collection: records.RecordCollection) -> Optional[int]:
    """Finds the ranking of a user in SELECT result"""
    for index, user_entry in enumerate(record_collection.all(as_dict=True)):
        if name == user_entry.get("name"):
            return index + 1
    return None


def create_select_query(table_name: str, where_key: str = None, where_value=None) -> str:
    """Create select statement from [table_name]"""
    if where_key is not None and where_value is not None:
        return f"select * FROM {table_name} WHERE {where_key}={where_value}"
    else:
        return f"select * FROM {table_name}"


def create_select_top_x_scores_query(table_name: str, limit: int = None) -> str:
    """Fetches every player's latest submission ranked from highest score to lowest score"""
    if limit is None:
        return f"SELECT score_table.* FROM {table_name} score_table WHERE score_table.id = (SELECT MAX(score_table2.id) FROM {table_name} score_table2 WHERE score_table2.name = score_table.name) ORDER BY score DESC, id"
    else:
        return f"SELECT score_table.* FROM {table_name} score_table WHERE score_table.id = (SELECT MAX(score_table2.id) FROM {table_name} score_table2 WHERE score_table2.name = score_table.name) ORDER BY score DESC, id LIMIT {limit}"


def create_update_query(table_name: str, column: str, new_value: str, where_key: str, where_value: str):
    """Create update statement for a value in a table"""
    return f"UPDATE {table_name} SET {column}={new_value} WHERE {where_key}={where_value}"


def create_delete_query(table_name: str, where_key: str, where_value: str):
    """Create update statement for a value in a table"""
    return f"DELETE FROM {table_name} WHERE {where_key}={where_value}"


# TODO: can't close connection after query because then it crashes while it's still attempting to retrieve data
def execute_statement(statement: str) -> records.RecordCollection:
    db = records.Database(common.DATABASE_CONNECTION)
    return db.query(statement)


def execute_statements(statements: List[str]) -> List[records.RecordCollection]:
    db = records.Database(common.DATABASE_CONNECTION)
    result_set = []

    for statement in statements:
        result_set.append(db.query(statement))
    return result_set