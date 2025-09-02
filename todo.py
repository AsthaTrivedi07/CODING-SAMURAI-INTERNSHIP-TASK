import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced To-Do App")
        self.root.geometry("600x650")
        self.root.configure(bg="#1e1e2f")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6, relief="flat",
                        background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#45a049")])

        # Data structure
        self.tasks = []

        # Title
        self.label = tk.Label(root, text="📌 To-Do List", font=("Segoe UI", 20, "bold"),
                              bg="#1e1e2f", fg="white")
        self.label.pack(pady=10)

        # Search bar
        self.search_entry = ttk.Entry(root, width=30, font=("Segoe UI", 12))
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_tasks)

        # Treeview (for category, deadline, status)
        columns = ("Task", "Category", "Due", "Status")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
        self.tree.pack(pady=10, fill="both", expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Input field
        self.task_entry = ttk.Entry(root, width=40, font=("Segoe UI", 12))
        self.task_entry.pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="✔ Mark Done", command=self.mark_done).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="🗑 Delete", command=self.delete_task).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="💾 Save JSON", command=self.save_json).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="📂 Load JSON", command=self.load_json).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="📊 Stats", command=self.show_stats).grid(row=1, column=2, padx=5, pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(root, length=400, mode="determinate")
        self.progress.pack(pady=10)

    # ------------------ Core Functions ------------------
    def add_task(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return

        category = simpledialog.askstring("Category", "Enter task category (Work/Personal/Study):")
        due_date = simpledialog.askstring("Deadline", "Enter due date (YYYY-MM-DD):")

        try:
            if due_date:
                datetime.strptime(due_date, "%Y-%m-%d")  # validate date
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        task = {"task": task_name, "category": category or "General",
                "due": due_date or "None", "status": "Pending"}

        self.tasks.append(task)
        self.refresh_tree()
        self.task_entry.delete(0, tk.END)

    def mark_done(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected)
            self.tasks[index]["status"] = "✔ Done"
            self.refresh_tree()
        else:
            messagebox.showwarning("Warning", "Select a task to mark done.")

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            index = self.tree.index(selected)
            del self.tasks[index]
            self.refresh_tree()
        else:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def save_json(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4)
        messagebox.showinfo("Saved", "Tasks saved to tasks.json")

    def load_json(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
            self.refresh_tree()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved tasks found.")

    def filter_tasks(self, event):
        query = self.search_entry.get().lower()
        self.refresh_tree(query)

    def refresh_tree(self, query=""):
        self.tree.delete(*self.tree.get_children())
        done_count = 0

        for task in self.tasks:
            if query in task["task"].lower() or query in task["category"].lower():
                self.tree.insert("", tk.END, values=(task["task"], task["category"], task["due"], task["status"]))
            if task["status"] == "✔ Done":
                done_count += 1

        if self.tasks:
            progress_value = (done_count / len(self.tasks)) * 100
            self.progress["value"] = progress_value
        else:
            self.progress["value"] = 0

    def show_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["status"] == "✔ Done")
        pending = total - done
        messagebox.showinfo("Task Stats", f"📊 Total: {total}\n✔ Done: {done}\n⏳ Pending: {pending}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
