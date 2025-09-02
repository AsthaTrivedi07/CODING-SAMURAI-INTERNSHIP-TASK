import tkinter as tk
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2f")

        # Variables
        self.secret_number = None
        self.attempts = 0
        self.running = False
        self.max_number = 100

        # Animated background canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="#1e1e2f", highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.circles = []
        self.animate_background()

        # UI Frame (on top of canvas)
        self.ui_frame = tk.Frame(root, bg="#2e2e44")
        self.ui_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = tk.Label(self.ui_frame, text="🎯 Number Guessing Game 🎯", 
                                    font=("Arial", 22, "bold"), fg="white", bg="#2e2e44")
        self.title_label.pack(pady=10)

        # Difficulty selection
        self.difficulty_frame = tk.Frame(self.ui_frame, bg="#2e2e44")
        self.difficulty_frame.pack(pady=5)

        tk.Label(self.difficulty_frame, text="Select Difficulty:", 
                 font=("Arial", 12), bg="#2e2e44", fg="white").pack(side="left", padx=5)

        self.difficulty_var = tk.StringVar(value="Easy")
        for level, rng in [("Easy", 50), ("Medium", 100), ("Hard", 200)]:
            tk.Radiobutton(self.difficulty_frame, text=level, variable=self.difficulty_var, 
                           value=level, font=("Arial", 10), bg="#2e2e44", fg="white",
                           selectcolor="#444", command=self.set_difficulty).pack(side="left", padx=5)

        # Entry + Guess button
        self.entry = tk.Entry(self.ui_frame, font=("Arial", 14), width=10, justify="center")
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        self.guess_button = tk.Button(self.ui_frame, text="Guess", font=("Arial", 12, "bold"), 
                                      bg="#4CAF50", fg="white", command=self.check_guess)
        self.guess_button.pack(pady=5)

        # Feedback
        self.feedback_label = tk.Label(self.ui_frame, text="", font=("Arial", 14, "bold"), 
                                       bg="#2e2e44", fg="yellow")
        self.feedback_label.pack(pady=10)

        # Guess log
        self.log_box = tk.Text(self.ui_frame, height=8, width=40, font=("Arial", 10), wrap="word", state="disabled")
        self.log_box.pack(pady=10)

        # Buttons
        self.button_frame = tk.Frame(self.ui_frame, bg="#2e2e44")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", font=("Arial", 12, "bold"),
                                      bg="#2196F3", fg="white", command=self.start_game)
        self.start_button.pack(side="left", padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", font=("Arial", 12, "bold"),
                                      bg="#FF5722", fg="white", command=self.reset_game)
        self.reset_button.pack(side="left", padx=5)

        self.quit_button = tk.Button(self.button_frame, text="Quit", font=("Arial", 12, "bold"),
                                     bg="#9C27B0", fg="white", command=root.quit)
        self.quit_button.pack(side="left", padx=5)

    def animate_background(self):
        """Simple floating circles animation."""
        for circle in self.circles:
            self.canvas.move(circle, 0, 1)
            x1, y1, x2, y2 = self.canvas.coords(circle)
            if y1 > 600:  # Reset circle to top
                self.canvas.move(circle, 0, -620)

        if len(self.circles) < 20:
            x = random.randint(0, 800)
            size = random.randint(10, 30)
            circle = self.canvas.create_oval(x, 0, x+size, size, fill="#444466", outline="")
            self.circles.append(circle)

        self.root.after(50, self.animate_background)

    def set_difficulty(self):
        level = self.difficulty_var.get()
        if level == "Easy":
            self.max_number = 50
        elif level == "Medium":
            self.max_number = 100
        else:
            self.max_number = 200

    def start_game(self):
        self.set_difficulty()
        self.secret_number = random.randint(1, self.max_number)
        self.attempts = 0
        self.running = True
        self.feedback_label.config(text=f"Game started! Guess between 1 and {self.max_number}")
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")

    def reset_game(self):
        self.secret_number = None
        self.attempts = 0
        self.running = False
        self.entry.delete(0, tk.END)
        self.feedback_label.config(text="Game reset. Click Start to play!")
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.config(state="disabled")

    def check_guess(self):
        if not self.running:
            self.feedback_label.config(text="Click Start to begin!")
            return

        try:
            guess = int(self.entry.get())
        except ValueError:
            self.feedback_label.config(text="Enter a valid number!")
            return

        self.attempts += 1
        self.entry.delete(0, tk.END)

        if guess == self.secret_number:
            self.feedback_label.config(text=f"🎉 Correct! You guessed it in {self.attempts} tries!")
            self.running = False
            self.log(f"✅ {guess} is Correct!")
        else:
            diff = abs(self.secret_number - guess)
            if guess < self.secret_number:
                hint = "LOW" if diff <= 10 else "TOO LOW"
            else:
                hint = "HIGH" if diff <= 10 else "TOO HIGH"

            self.feedback_label.config(text=f"{hint}! Try again.")
            self.log(f"❌ {guess} → {hint}")

    def log(self, message):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()
