"""
Clash of Code Admin GUI
A tkinter-based admin panel for managing database tables.
Provides CRUD operations for Users, Matches, Submissions, and Ratings.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Import models
from app.database.models.user import User
from app.database.models.match import Match
from app.database.models.submission import Submission
from app.database.models.rating import Rating
from app.database.models.analytics import Analytics

# Try to import hash_password, with fallback
try:
    from app.core.security import hash_password
except ImportError:
    # Fallback if passlib not installed
    def hash_password(password: str) -> str:
        return password  # WARNING: Not secure, only for demo

# Load environment variables (prefer backend/app/.env when present)
env_path = os.path.join(os.path.dirname(__file__), "app", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# ==================== DATABASE SETUP ====================
# construct a default path pointing to project root clash.db
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
default_db_path = os.path.join(project_root, "clash.db")
# sqlite url must have four slashes for absolute path
default_db_url = f"sqlite:///{default_db_path}"

raw_db_url = os.getenv("DATABASE_URL", default_db_url)  # can override via .env

# If .env contains an asyncpg URL (used by async code elsewhere), convert
# to a sync-compatible URL for this synchronous admin GUI (requires psycopg2).
if isinstance(raw_db_url, str) and raw_db_url.startswith("postgresql+asyncpg://"):
    DATABASE_URL = raw_db_url.replace("+asyncpg", "")
else:
    DATABASE_URL = raw_db_url

try:
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✓ Database connection successful!")
except Exception as e:
    messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
    sys.exit(1)

# ==================== MAIN WINDOW ====================
root = tk.Tk()
root.title("Clash of Code - Admin Panel")
root.geometry("1200x800")
root.config(bg="#f0f0f0")

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# ==================== HELPER FUNCTIONS ====================

def refresh_tree(tree, model, columns, session_obj=None):
    """Refresh the treeview with data from the database."""
    if session_obj is None:
        session_obj = session
    
    for row in tree.get_children():
        tree.delete(row)
    
    try:
        objects = session_obj.query(model).all()
        for obj in objects:
            values = []
            for col in columns:
                if col == "password":
                    values.append("***")
                else:
                    val = getattr(obj, col, "")
                    # Format datetime objects
                    if isinstance(val, datetime):
                        values.append(val.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        values.append(str(val) if val is not None else "")
            tree.insert("", tk.END, values=values)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

def create_add_edit_dialog(model, columns, tree, session_obj=None, obj=None):
    """Create a dialog to add or edit records."""
    if session_obj is None:
        session_obj = session
    
    def save_record():
        try:
            obj_or_new = obj if obj else model()
            
            for col in columns:
                if col == "id" or col == "created_at":
                    continue
                
                widget = entries.get(col)
                if not widget:
                    continue
                
                value = widget.get()
                
                # Handle special cases
                if col == "password" and value:
                    value = hash_password(value)
                elif col in ["user_id", "match_id", "score"]:
                    try:
                        value = int(value) if value else None
                    except ValueError:
                        messagebox.showerror("Input Error", f"{col} must be a number")
                        return
                
                setattr(obj_or_new, col, value)
            
            if not obj:
                session_obj.add(obj_or_new)
            
            session_obj.commit()
            messagebox.showinfo("Success", "Record saved successfully!")
            refresh_tree(tree, model, columns, session_obj)
            dialog_window.destroy()
        
        except SQLAlchemyError as e:
            session_obj.rollback()
            messagebox.showerror("Database Error", f"Failed to save record:\n{e.orig}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
    
    def cancel():
        dialog_window.destroy()
    
    # Create dialog window
    dialog_window = tk.Toplevel(root)
    dialog_window.title("Edit Record" if obj else "Add New Record")
    dialog_window.geometry("400x500")
    
    # Create scrolled frame
    canvas = tk.Canvas(dialog_window)
    scrollbar = ttk.Scrollbar(dialog_window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Add input fields
    entries = {}
    for i, col in enumerate(columns):
        if col == "id" or col == "created_at":
            continue
        
        label = ttk.Label(scrollable_frame, text=f"{col.replace('_', ' ').title()}:")
        label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
        
        if col == "code":
            # Use text widget for code
            text_widget = scrolledtext.ScrolledText(scrollable_frame, height=5, width=40)
            text_widget.grid(row=i, column=1, padx=10, pady=5)
            if obj:
                text_widget.insert("1.0", getattr(obj, col, ""))
            entries[col] = text_widget
        elif col == "password":
            # Use Entry with show for password
            entry = ttk.Entry(scrollable_frame, show="*")
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            entries[col] = entry
        else:
            entry = ttk.Entry(scrollable_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=5)
            if obj:
                value = getattr(obj, col, "")
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                entry.insert(0, str(value) if value is not None else "")
            entries[col] = entry
    
    # Buttons frame
    button_frame = ttk.Frame(scrollable_frame)
    button_frame.grid(row=len(columns), column=0, columnspan=2, pady=20)
    
    ttk.Button(button_frame, text="Save", command=save_record).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

def edit_selected_record(model, tree, columns, session_obj=None):
    """Edit the selected record."""
    if session_obj is None:
        session_obj = session
    
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to edit")
        return
    
    item = tree.item(selected[0])
    obj_id = item["values"][0]
    
    obj = session_obj.get(model, obj_id)
    if obj:
        create_add_edit_dialog(model, columns, tree, session_obj, obj)

def delete_selected_record(model, tree, session_obj=None):
    """Delete the selected record."""
    if session_obj is None:
        session_obj = session
    
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a record to delete")
        return
    
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
        try:
            for sel in selected:
                item = tree.item(sel)
                obj_id = item["values"][0]
                obj = session_obj.get(model, obj_id)
                if obj:
                    session_obj.delete(obj)
            session_obj.commit()
            messagebox.showinfo("Success", "Record deleted successfully!")
            refresh_tree(tree, model, tree["columns"], session_obj)
        except SQLAlchemyError as e:
            session_obj.rollback()
            messagebox.showerror("Database Error", f"Failed to delete record:\n{e.orig}")

def create_table_tab(parent, model, columns):
    """Create a tab with table view and CRUD buttons."""
    # Main frame with gridding
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill="both", expand=True)
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill="x", padx=10, pady=10)
    
    # Create treeview frame
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Create treeview
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    
    # Define columns
    for col in columns:
        col_width = 150 if col != "code" else 300
        tree.column(col, width=col_width)
        tree.heading(col, text=col.replace("_", " ").title())
    
    # Add scrollbars
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    # Grid layout for tree frame
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    # Create buttons
    ttk.Button(
        button_frame,
        text="➕ Add Record",
        command=lambda: create_add_edit_dialog(model, columns, tree)
    ).pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        button_frame,
        text="✏️ Edit Record",
        command=lambda: edit_selected_record(model, tree, columns)
    ).pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        button_frame,
        text="🗑️ Delete Record",
        command=lambda: delete_selected_record(model, tree)
    ).pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        button_frame,
        text="🔄 Refresh",
        command=lambda: refresh_tree(tree, model, columns)
    ).pack(side=tk.LEFT, padx=5)
    
    # Load initial data
    refresh_tree(tree, model, columns)
    
    return main_frame

# ==================== CREATE TABS ====================
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Users Tab
users_columns = ["id", "username", "email", "hashed_password", "created_at"]
users_tab = ttk.Frame(notebook)
notebook.add(users_tab, text="👥 Users")
create_table_tab(users_tab, User, users_columns)

# Matches Tab
matches_columns = ["id", "name", "created_by_id", "created_at"]
matches_tab = ttk.Frame(notebook)
notebook.add(matches_tab, text="🎮 Matches")
create_table_tab(matches_tab, Match, matches_columns)

# Submissions Tab
submissions_columns = ["id", "user_id", "match_id", "code", "created_at"]
submissions_tab = ttk.Frame(notebook)
notebook.add(submissions_tab, text="📝 Submissions")
create_table_tab(submissions_tab, Submission, submissions_columns)

# Ratings Tab
ratings_columns = ["id", "user_id", "match_id", "score"]
ratings_tab = ttk.Frame(notebook)
notebook.add(ratings_tab, text="⭐ Ratings")
create_table_tab(ratings_tab, Rating, ratings_columns)

# Analytics Tab
analytics_columns = ["id", "user_id", "match_id", "score", "created_at"]
analytics_tab = ttk.Frame(notebook)
notebook.add(analytics_tab, text="📊 Analytics")
create_table_tab(analytics_tab, Analytics, analytics_columns)

# Status bar
status_frame = ttk.Frame(root)
status_frame.pack(fill="x", padx=10, pady=5)
status_label = ttk.Label(status_frame, text=f"Connected to: {DATABASE_URL[:50]}...", relief="sunken")
status_label.pack(fill="x")

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    root.mainloop()
    session.close()