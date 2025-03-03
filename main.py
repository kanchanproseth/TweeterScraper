import tkinter as tk
from tkinter import filedialog, Label, Button, ttk
import pandas as pd
from helper.tweeter_scraper_helper import *
from copy_able_tree_view import *
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tweeter Scaper")
        self.root.geometry("800x500")
        
        def start_task():
            thread = threading.Thread(target=self.export_file, daemon=True)
            thread.start()

        # Label to show selected file
        self.label = Label(root, text="No file selected", wraplength=700)
        self.label.pack(pady=10)

        # Browse Button
        self.browse_button = Button(root, text="Browse Excel File", command=self.browse_file)
        self.browse_button.pack(pady=5)
        
        # Export Button (Export the updated file)
        self.export_button = Button(root, text="Export Updated File", command=start_task, state=tk.DISABLED)
        self.export_button.pack(pady=5)

        # Process Button
        self.process_button = Button(root, text="Load Data", command=self.process_file, state=tk.DISABLED)
        self.process_button.pack(pady=5)

        # Frame for Table and Scrollbars
        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        # Scrollbars
        self.tree_scroll_y = ttk.Scrollbar(self.table_frame, orient="vertical")
        self.tree_scroll_x = ttk.Scrollbar(self.table_frame, orient="horizontal")

        # Treeview for Data Table
        self.tree = CopyableTreeview(
            self.table_frame,
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
            show="headings"
        )

        # Attach Scrollbars to Treeview
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Pack Scrollbars and Treeview
        self.tree_scroll_y.pack(side="right", fill="y")
        self.tree_scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        self.selected_file = None  # Store the selected file path
        self.df = None

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            self.selected_file = file_path
            self.label.config(text=f"Selected File: {file_path}")
            self.process_button.config(state=tk.NORMAL)  # Enable the process button

    def process_file(self):
        
        if self.selected_file:
            try:
                self.df = pd.read_excel(self.selected_file)  # Read the Excel file
                self.df.fillna('', inplace=True)
                self.reset_data_table()
                thread = threading.Thread(target=self.fetch_data, daemon=True)
                thread.start()
            except Exception as e:
                self.label.config(text=f"Error loading file: {e}")
                
    def fetch_data(self):
        for index, row in self.df.iterrows():
            self.root.after(0, self.update_label, f"Retrieving data in row: {index}")
            print(f"Row {index}:")
            print(f"Link: {row['tweeter_url']}")
            tweeter_url = row['tweeter_url']
            result = get_twitter_metrics(tweeter_url)
            clutch_point_sub_string = '/ClutchPoints/status'.lower()
            if clutch_point_sub_string in tweeter_url.lower():
                self.df.at[index, "CP (Y/N)"] = 'YES'
            else:
                self.df.at[index, "CP (Y/N)"] = 'NO'
            
            if "error" in result:
                print(f"Error occurred: {result['error']}")
                self.root.after(0, self.update_label, f"Error getting data: {result}")
            else:
                print(f"Likes: {result['like']}, Retweets: {result['retweet']}")
                self.df.at[index, "LIKES"] = result['like']
                self.df.at[index, "RTs"] = result['retweet']
        self.root.after(0, self.update_label, f"All row processing is completed")
                
        self.display_table()
        
    def reset_data_table(self):
         # Clear existing table
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        
    def display_table(self):
        # Define column headings
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)  # Adjust column width

        # Insert all rows into the table        
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.export_button.config(state=tk.NORMAL)
            
    def update_label(self, text):
        self.label.config(text=text)
            
    def export_file(self):
        if self.df is not None and self.selected_file:
            try:
                # Save the updated dataframe to the same file
                self.df.to_excel(self.selected_file, index=False)
                self.root.after(0, self.update_label, f"File updated successfully: {self.selected_file}")
            except Exception as e:
                self.root.after(0, self.update_label, f"Error saving file: {e}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()