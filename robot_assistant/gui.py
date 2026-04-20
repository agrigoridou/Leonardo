import tkinter as tk
import random

class RobotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.eye_radius = 80
        self.pupil_radius = 20

        self.draw_face()

    def draw_face(self):
        self.canvas.delete("all")

        lx, ly = self.width//3, self.height//2
        rx, ry = 2*self.width//3, self.height//2

        # μάτια
        self.left_eye = self.canvas.create_oval(
            lx-80, ly-80, lx+80, ly+80, fill="white"
        )
        self.right_eye = self.canvas.create_oval(
            rx-80, ry-80, rx+80, ry+80, fill="white"
        )

        # κόρες
        self.left_pupil = self.canvas.create_oval(
            lx-20, ly-20, lx+20, ly+20, fill="black"
        )
        self.right_pupil = self.canvas.create_oval(
            rx-20, ry-20, rx+20, ry+20, fill="black"
        )

        # στόμα
        self.mouth = self.canvas.create_arc(
            self.width//2 - 100, self.height//2 + 100,
            self.width//2 + 100, self.height//2 + 200,
            start=0, extent=-180, style="arc", width=5
        )

    def move_eyes(self):
        dx = random.randint(-20, 20)
        dy = random.randint(-20, 20)

        self.canvas.move(self.left_pupil, dx, dy)
        self.canvas.move(self.right_pupil, dx, dy)

        self.root.after(500, self.move_eyes)

    def talking(self):
        self.canvas.itemconfig(self.mouth, extent=-120)
        self.root.update()

    def idle(self):
        self.canvas.itemconfig(self.mouth, extent=-180)
        self.root.update()

    def listening(self):
        self.canvas.itemconfig(self.mouth, extent=-60)
        self.root.update()

    def error(self):
        self.canvas.itemconfig(self.mouth, extent=180)
        self.root.update()

    def run(self):
        self.move_eyes()
        self.root.mainloop()
