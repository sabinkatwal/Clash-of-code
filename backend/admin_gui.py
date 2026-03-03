import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.models import user, match, submission, rating
from app.database.base import Base

# -------------------- DATABASE SETUP --------------------
DATABASE_URL = "postgresql://clash_user:sabindon@localhost:5432/clash_of_code"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# -------------------- MAIN APP --------------------
root = tk.Tk()
root.title("Clash of Code Admin Panel")
root.geometry("900x600")

# -------------------- TAB CONTROL --------------------
tab_control = ttk.Notebook(root)
tab_users = ttk.Frame(tab_control)
tab_matches = ttk.Frame(tab_control)
tab_submissions = ttk.Frame(tab_control)
tab_ratings = ttk.Frame(tab_control)
tab_control.add(tab_users, text="Users")
tab_control.add(tab_matches, text="Matches")
tab_control.add(tab_submissions, text="Submissions")
tab_control.add(tab_ratings, text="Ratings")
tab_control.pack(expand=1, fill="both")

# -------------------- HELPER FUNCTIONS --------------------
def refresh_tree(tree, model):
    for row in tree.get_children():
        tree.delete(row)
    for obj in session.query(model).all():
        values = [getattr(obj, col) for col in tree["columns"]]
        tree.insert("", tk.END, values=values)

def add_user():
    def save():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            new_user = user.User(username=username, password=password)
            session.add(new_user)
            session.commit()
            refresh_tree(tree_users, user.User)
            add_win.destroy()
        else:
            messagebox.showerror("Error", "All fields required")
    add_win = tk.Toplevel(root)
    add_win.title("Add User")
    tk.Label(add_win, text="Username").grid(row=0, column=0)
    tk.Label(add_win, text="Password").grid(row=1, column=0)
    entry_username = tk.Entry(add_win)
    entry_username.grid(row=0, column=1)
    entry_password = tk.Entry(add_win)
    entry_password.grid(row=1, column=1)
    tk.Button(add_win, text="Save", command=save).grid(row=2, column=0, columnspan=2)

# -------------------- USERS TAB --------------------
columns = ["id", "username", "password"]
tree_users = ttk.Treeview(tab_users, columns=columns, show="headings")
for col in columns:
    tree_users.heading(col, text=col)
tree_users.pack(expand=1, fill="both")
refresh_tree(tree_users, user.User)

tk.Button(tab_users, text="Add User", command=add_user).pack()

# -------------------- MATCHES TAB --------------------
columns = ["id", "name", "created_by_id"]
tree_matches = ttk.Treeview(tab_matches, columns=columns, show="headings")
for col in columns:
    tree_matches.heading(col, text=col)
tree_matches.pack(expand=1, fill="both")
refresh_tree(tree_matches, match.Match)

# -------------------- SUBMISSIONS TAB --------------------
columns = ["id", "user_id", "match_id", "code"]
tree_submissions = ttk.Treeview(tab_submissions, columns=columns, show="headings")
for col in columns:
    tree_submissions.heading(col, text=col)
tree_submissions.pack(expand=1, fill="both")
refresh_tree(tree_submissions, submission.Submission)

# -------------------- RATINGS TAB --------------------
columns = ["id", "user_id", "match_id", "score"]
tree_ratings = ttk.Treeview(tab_ratings, columns=columns, show="headings")
for col in columns:
    tree_ratings.heading(col, text=col)
tree_ratings.pack(expand=1, fill="both")
refresh_tree(tree_ratings, rating.Rating)

# -------------------- RUN APP --------------------
root.mainloop()