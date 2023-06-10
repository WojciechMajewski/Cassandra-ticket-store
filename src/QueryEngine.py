import uuid

class QueryEngine:
    def INSERT(self, table_name, table_cols, table_col_type, values):
        #this is needed because some values have spaces and it broke the system
        values_formatted = ""
        for i in range(len(values)):
            if table_col_type[i] == 'text' or table_col_type[i] == 'timestamp':
                val = f"'{values[i]}'"
            else:
                val = f"{values[i]}"
            values_formatted += val
            if (i != len(values) - 1):
                values_formatted += ", "
        query = f"INSERT INTO {table_name} ({', '.join(table_cols)}) VALUES ({values_formatted})"
        return query

    def UPDATE(self, table_name, table_col, table_col_type, value_updated, column_where, column_where_type, value_where):
        if table_col_type == 'text' or table_col_type == 'timestamp':
            val_updated = f"'{value_updated}'"
        else:
            val_updated = f"{value_updated}"
        if column_where_type == 'text' or column_where_type == 'timestamp':
            val_where = f"'{value_where}'"
        else:
            val_where = f"{value_where}"
        query = f"UPDATE {table_name} SET {table_col} = {val_updated} "
        query += f"WHERE {column_where} = {val_where} IF EXISTS;"
        return query

    def SELECT_ALL(self, table_name):
        query = f"SELECT * FROM {table_name};"
        return query

    def SELECT_COLUMNS(self, table_name, table_columns):
        query = f"SELECT {', '.join(table_columns)} FROM {table_name};"
        return query

    def SELECT_WHERE(self, table_name, column_where, column_where_type, value_where):
        if column_where_type == 'text' or column_where_type == 'timestamp':
            val_where = f"'{value_where}'"
        else:
            val_where = f"{value_where}"
        query = f"SELECT * FROM {table_name} WHERE {column_where} = {val_where} ALLOW FILTERING; "
        return query
    
    def DELETE(self, table_name, column_where, column_where_type, value_where):
        query = f"DELETE FROM {table_name} WHERE {column_where} = {value_where} IF EXISTS;"
        return query