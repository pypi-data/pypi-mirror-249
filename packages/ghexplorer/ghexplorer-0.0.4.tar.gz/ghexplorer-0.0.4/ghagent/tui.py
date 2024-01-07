from ghagent.util.conversion import df_to_textual_table
import pandas as pd
from textual.app import App
from textual.widgets import Header, Footer, DataTable, Label
from textual.widget import Widget
from textual.binding import Binding


DUMMY_ROWS = pd.DataFrame(data=[
    [4, "Joseph Schooling", "Singapore", 50.39],
    [2, "Michael Phelps", "United States", 51.14],
    [5, "Chad le Clos", "South Africa", 51.14],
    [6, "László Cseh", "Hungary", 51.14],
    [3, "Li Zhuhao", "China", 51.26],
    [8, "Mehdy Metella", "France", 51.58],
    [7, "Tom Shields", "United States", 51.73],
    [1, "Aleksandr Sadovnikov", "Russia", 51.84],
    [10, "Darren Burns", "Scotland", 51.84],
], columns=["lane", "swimmer", "country", "time"])

class DFTable(Widget):
    """
    Table with a pandas DataFrame as its data source
    """
    def __init__(self, data: pd.DataFrame, show_table_name: bool, table_name: str):
        super().__init__()
        self.data = data
        self.show_table_name = show_table_name
        self.table_name = table_name
    
    def compose(self):
        if self.show_table_name:
            yield Label(renderable=self.table_name, classes="table_name")
        
        data_table = DataTable(show_cursor=False)
        data_table = df_to_textual_table(self.data, data_table)
        yield data_table

class GHAgentApp(App):
    CSS_PATH = "tui.tcss"
    
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
    ]
    
    def __init__(self, relevant_related_repos, potential_stargazers):
        super().__init__()
        self.relevant_related_repos = relevant_related_repos
        self.potential_stargazers = potential_stargazers
    
    def compose(self):
        yield Header()
        
        yield DFTable(data=self.relevant_related_repos, show_table_name=True, table_name="Related Repos")
        yield DFTable(data=self.potential_stargazers, show_table_name=True, table_name="Potential Stargazers")
        
        yield Footer()

if __name__ == "__main__":
    app = GHAgentApp(relevant_related_repos=DUMMY_ROWS, potential_stargazers=DUMMY_ROWS)
    app.run()
