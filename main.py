import json
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


def fetch_data():
    global table1_data, table2_data
    conn1 = sqlite3.connect('database1.db')
    cursor1 = conn1.cursor()
    cursor1.execute('SELECT * FROM table1')
    table1_data = cursor1.fetchall()
    conn1.close()

    conn2 = sqlite3.connect('database2.db')
    cursor2 = conn2.cursor()
    cursor2.execute('SELECT * FROM table2')
    table2_data = cursor2.fetchall()
    conn2.close()

    display_data()


def display_data():
    for row in table1_tree.get_children():
        table1_tree.delete(row)
    for row in table2_tree.get_children():
        table2_tree.delete(row)

    for row in table1_data:
        table1_tree.insert('', 'end', values=row)

    for row in table2_data:
        table2_tree.insert('', 'end', values=row)


def sync_databases():
    try:
        with open('mapping_config.json', 'r') as f:
            mapping = json.load(f)

        conn1 = sqlite3.connect('database1.db')
        cursor1 = conn1.cursor()
        cursor1.execute('SELECT * FROM table1')
        table1_data = cursor1.fetchall()

        conn2 = sqlite3.connect('database2.db')
        cursor2 = conn2.cursor()

        cursor2.execute('DELETE FROM table2')

        for row in table1_data:
            mapped_row = [None] * 6
            for col1, col2 in mapping.items():
                source_index = int(col1[6:]) - 1 
                target_index = int(col2[6:]) - 21
                mapped_row[target_index] = row[source_index]
            cursor2.execute('''INSERT INTO table2 (column21, column22, column23, column24, column25, column26)
                               VALUES (?, ?, ?, ?, ?, ?)''', tuple(mapped_row))
        conn2.commit()
        conn2.close()
        conn1.close()
        messagebox.showinfo("Sync", "Databases synchronized successfully!")
    except Exception as e:
        messagebox.showerror("Sync Error", str(e))

    reset_timer()


def update_timer_label():
    timer_label.config(text=f"{minutes.get():02d}:{seconds.get():02d}")


def start_timer():
    global timer_id
    if minutes.get() == 0 and seconds.get() == 0:
        sync_databases()
    else:
        if seconds.get() == 0:
            minutes.set(minutes.get() - 1)
            seconds.set(59)
        else:
            seconds.set(seconds.get() - 1)
        update_timer_label()
        timer_id = root.after(1000, start_timer)


def reset_timer():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
    minutes.set(5)
    seconds.set(0)
    update_timer_label()
    start_timer()

root = tk.Tk()
root.title("Database Column Mapper")

timer_id = None

minutes = tk.IntVar(value=5)
seconds = tk.IntVar(value=0)
timer_label = tk.Label(root, font=("Arial", 20))
timer_label.pack(pady=10)

frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, padx=20, pady=20)
frame2 = tk.Frame(root)
frame2.pack(side=tk.RIGHT, padx=20, pady=20)

table1_tree = ttk.Treeview(frame1, columns=(1, 2, 3, 4, 5, 6), show='headings', height=10)
table1_tree.column(1, width=65)
table1_tree.column(2, width=65)
table1_tree.column(3, width=65)
table1_tree.column(4, width=65)
table1_tree.column(5, width=65)
table1_tree.column(6, width=65)
table1_tree.pack()
for i in range(1, 7):
    table1_tree.heading(i, text=f'Column {i}')

table2_tree = ttk.Treeview(frame2, columns=(21, 22, 23, 24, 25, 26), show='headings', height=10)
table2_tree.column(21, width=65)
table2_tree.column(22, width=65)
table2_tree.column(23, width=65)
table2_tree.column(24, width=65)
table2_tree.column(25, width=65)
table2_tree.column(26, width=65)
table2_tree.pack()
for i in range(21, 27):
    table2_tree.heading(i, text=f'Column {i}')

fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.pack(pady=10)

mapping_frame = tk.Frame(root)
mapping_frame.pack(pady=20)

mapping_label = tk.Label(mapping_frame, text="Column Mapping:")
mapping_label.grid(row=0, column=0, columnspan=2)

table1_columns = [f'column{i}' for i in range(1, 7)]
table2_columns = [f'column2{i}' for i in range(1, 7)]

mapping_vars = {}
for i, col1 in enumerate(table1_columns):
    mapping_vars[col1] = tk.StringVar()
    tk.Label(mapping_frame, text=col1).grid(row=i + 1, column=0)
    mapping_vars[col1].set(table2_columns[i])
    tk.OptionMenu(mapping_frame, mapping_vars[col1], *table2_columns).grid(row=i + 1, column=1)


def save_mapping():
    mapping = {col: var.get() for col, var in mapping_vars.items()}
    with open('mapping_config.json', 'w') as f:
        json.dump(mapping, f)
    messagebox.showinfo("Save Mapping", "Mapping configuration saved successfully!")


def load_mapping():
    try:
        with open('mapping_config.json', 'r') as f:
            mapping = json.load(f)
            for col, var in mapping_vars.items():
                var.set(mapping[col])
    except FileNotFoundError:
        messagebox.showwarning("Load Mapping", "No saved mapping configuration found.")


save_button = tk.Button(root, text="Save Mapping", command=save_mapping)
save_button.pack(pady=10)

load_button = tk.Button(root, text="Load Mapping", command=load_mapping)
load_button.pack(pady=10)

sync_button = tk.Button(root, text="Sync Databases", command=sync_databases)
sync_button.pack(pady=10)

load_mapping()

reset_timer()

root.mainloop()
