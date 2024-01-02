from typing import Optional
import pandas as pd
from rich.table import Table
from textual.widgets import DataTable

# Reference: https://gist.github.com/neelabalan/33ab34cf65b43e305c3f12ec6db05938
def df_to_rich_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.
    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values."""

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table

def df_to_textual_table(
    pandas_dataframe: pd.DataFrame,
    textual_table: DataTable,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> DataTable:
    """Convert a pandas.DataFrame obj into a textual.widgets.DataTable obj.
    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a textual DataTable.
        textual_table (DataTable): A textual DataTable that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        DataTable: The textual DataTable instance passed, populated with the DataFrame values."""
    
    if show_index:
        index_name = str(index_name) if index_name else ""
        textual_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        textual_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.values.tolist()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list]
        textual_table.add_row(*row)

    return textual_table
