import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from neomodel import config, db
from models import School, Stop
from credentials import Credentials

config.DATABASE_URL = Credentials.getNeo4JDatabaseURI()

class SchoolRatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Find School-Rating")
        self.root.geometry("600x450")

        self.style = ttk.Style(self.root)
        self.style.theme_use('equilux')

        header_label = tk.Label(root, text="Find School-Rating", font=("Helvetica", 16))
        header_label.pack(pady=10)

        self.search_var = tk.StringVar()
        self.combobox = ttk.Combobox(root, textvariable=self.search_var)
        self.combobox.pack(pady=10, padx=20)
        self.combobox.bind('<KeyRelease>', self.update_dropdown)

        self.result_text = tk.Text(root, wrap="word", height=10, width=60, bg="#f0f0f0")
        self.result_text.pack(pady=10, padx=20)

        search_button = ttk.Button(root, text="Find Rating", command=self.display_rating)
        search_button.pack(pady=5)

        self.update_dropdown()

    def update_dropdown(self, event=None):
        substring = self.search_var.get().strip().lower()

        if substring:
            query = f"MATCH (s:School) WHERE toLower(s.name) CONTAINS '{substring}' RETURN s ORDER BY s.name DESC"
        else:
            query = "MATCH (s:School) RETURN s ORDER BY s.name DESC LIMIT 10"
        
        results, _ = db.cypher_query(query)
        school_names = [record[0]['name'] for record in results]

        self.combobox['values'] = school_names

    def display_rating(self):
        school_name = self.search_var.get().strip()

        if not school_name:
            return

        self.result_text.delete(1.0, tk.END)

        rating_query = f"""
        MATCH (s:School {{name: '{school_name}'}})
        RETURN s.rating as rating
        """
        rating_result, _ = db.cypher_query(rating_query)

        if rating_result and rating_result[0][0] is not None:
            rating = rating_result[0][0]
        else:
            rating = "No rating available"

        self.result_text.insert(tk.END, f'Rating overall for this School is: {rating}\n\n')

        query = f"""
        MATCH (s:School {{name: '{school_name}'}})-[r]->(stop:Stop)-[:HAS_LINE]->(line:Line)
        RETURN stop, r, collect(line.name) as lines
        """
        results, _ = db.cypher_query(query)

        if results:
            self.result_text.insert(tk.END, f"Bus Stops and Lines for {school_name}:\n\n")

            for stop, relation, lines in results:
                distance_type = "300m" if relation.type == 'IS_NEARBY' else "600m"
                stop_info = f"Stop: {stop['name']}, Distance: {distance_type}, Lines: {', '.join(lines)}\n"
                self.result_text.insert(tk.END, stop_info)
        else:
            self.result_text.insert(tk.END, "No stops found for this school.")

root = ThemedTk(theme="equilux")
app = SchoolRatingApp(root)
root.mainloop()
