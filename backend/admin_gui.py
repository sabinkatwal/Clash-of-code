import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import user, match, submission, rating
from app.database.base import Base

# -------------------- DATABASE --------------------
DATABASE_URL = "postgresql://clash_user:sabindon@localhost:5432/clash_of_code"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("Clash of Code Admin Panel")
root.geometry("1000x700")

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
def refresh_tree(tree, model, columns):
    for row in tree.get_children():
        tree.delete(row)
    for obj in session.query(model).all():
        values = [getattr(obj, col) for col in columns]
        tree.insert("", tk.END, values=values)

def add_edit_dialog(model, columns, tree, obj=None):
    """Generic add/edit dialog for any table"""
    def save():
        for col in columns[1:]:  # skip id
            value = entries[col].get()
            setattr(obj_or_new, col, value)
        if obj is None:
            session.add(obj_or_new)
        session.commit()
        refresh_tree(tree, model, columns)
        win.destroy()

    win = tk.Toplevel(root)
    win.title("Edit" if obj else "Add")
    entries = {}
    obj_or_new = obj or model()
    for i, col in enumerate(columns[1:]):  # skip id
        tk.Label(win, text=col).grid(row=i, column=0)
        entry = tk.Entry(win)
        entry.grid(row=i, column=1)
        entry.insert(0, getattr(obj_or_new, col, ""))
        entries[col] = entry
    tk.Button(win, text="Save", command=save).grid(row=len(columns), column=0, columnspan=2)

def delete_selected(model, tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a row to delete")
        return
    if messagebox.askyesno("Confirm", "Are you sure you want to delete?"):
        for sel in selected:
            item = tree.item(sel)
            obj_id = item["values"][0]
            obj = session.get(model, obj_id)
            if obj:
                session.delete(obj)
        session.commit()
        refresh_tree(tree, model, tree["columns"])

# -------------------- USERS TAB --------------------
user_columns = ["id", "username", "password"]
tree_users = ttk.Treeview(tab_users, columns=user_columns, show="headings")
for col in user_columns:
    tree_users.heading(col, text=col)
tree_users.pack(expand=1, fill="both")

tk.Button(tab_users, text="Add User", command=lambda: add_edit_dialog(user.User, user_columns, tree_users)).pack(side=tk.LEFT)
tk.Button(tab_users, text="Edit User", command=lambda: edit_selected(user.User, tree_users, user_columns)).pack(side=tk.LEFT)
tk.Button(tab_users, text="Delete User", command=lambda: delete_selected(user.User, tree_users)).pack(side=tk.LEFT)
refresh_tree(tree_users, user.User, user_columns)

# -------------------- MATCHES TAB --------------------
match_columns = ["id", "name", "created_by_id"]
tree_matches = ttk.Treeview(tab_matches, columns=match_columns, show="headings")
for col in match_columns:
    tree_matches.heading(col, text=col)
tree_matches.pack(expand=1, fill="both")

tk.Button(tab_matches, text="Add Match", command=lambda: add_edit_dialog(match.Match, match_columns, tree_matches)).pack(side=tk.LEFT)
tk.Button(tab_matches, text="Edit Match", command=lambda: edit_selected(match.Match, tree_matches, match_columns)).pack(side=tk.LEFT)
tk.Button(tab_matches, text="Delete Match", command=lambda: delete_selected(match.Match, tree_matches)).pack(side=tk.LEFT)
refresh_tree(tree_matches, match.Match, match_columns)

# -------------------- SUBMISSIONS TAB --------------------
submission_columns = ["id", "user_id", "match_id", "code"]
tree_submissions = ttk.Treeview(tab_submissions, columns=submission_columns, show="headings")
for col in submission_columns:
    tree_submissions.heading(col, text=col)
tree_submissions.pack(expand=1, fill="both")

tk.Button(tab_submissions, text="Add Submission", command=lambda: add_edit_dialog(submission.Submission, submission_columns, tree_submissions)).pack(side=tk.LEFT)
tk.Button(tab_submissions, text="Edit Submission", command=lambda: edit_selected(submission.Submission, tree_submissions, submission_columns)).pack(side=tk.LEFT)
tk.Button(tab_submissions, text="Delete Submission", command=lambda: delete_selected(submission.Submission, tree_submissions)).pack(side=tk.LEFT)
refresh_tree(tree_submissions, submission.Submission, submission_columns)

# -------------------- RATINGS TAB --------------------
rating_columns = ["id", "user_id", "match_id", "score"]
tree_ratings = ttk.Treeview(tab_ratings, columns=rating_columns, show="headings")
for col in rating_columns:
    tree_ratings.heading(col, text=col)
tree_ratings.pack(expand=1, fill="both")

tk.Button(tab_ratings, text="Add Rating", command=lambda: add_edit_dialog(rating.Rating, rating_columns, tree_ratings)).pack(side=tk.LEFT)
tk.Button(tab_ratings, text="Edit Rating", command=lambda: edit_selected(rating.Rating, tree_ratings, rating_columns)).pack(side=tk.LEFT)
tk.Button(tab_ratings, text="Delete Rating", command=lambda: delete_selected(rating.Rating, tree_ratings)).pack(side=tk.LEFT)
refresh_tree(tree_ratings, rating.Rating, rating_columns)

# -------------------- Edit Selected Helper --------------------
def edit_selected(model, tree, columns):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select a row to edit")
        return
    obj_id = tree.item(selected[0])["values"][0]
    obj = session.get(model, obj_id)
    if obj:
        add_edit_dialog(model, columns, tree, obj)

# -------------------- RUN APP --------------------
root.mainloop()