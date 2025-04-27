import tkinter as tk
from tkinter import simpledialog, messagebox
import os
from PIL import Image, ImageTk

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ––– Utilities for rounded-corner buttons on any background –––
def round_rectangle(canvas, x1, y1, x2, y2, radius=12, **kwargs):
    points = [
        x1+radius, y1,
        x1+radius, y1,
        x2-radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

class RoundButton(tk.Canvas):
    def __init__(self, parent, text="", radius=12, padding=8, bg="#A3C8F3", fg="black", font=("Arial",10), command=None):
        super().__init__(parent, highlightthickness=0, bg=parent["bg"])
        self.command = command
        # measure text
        tmp = self.create_text(0,0, text=text, font=font)
        bbox = self.bbox(tmp)
        self.delete(tmp)
        tw = bbox[2]-bbox[0]
        th = bbox[3]-bbox[1]
        w = tw + padding*2
        h = th + padding*2
        self.config(width=w, height=h)
        # draw
        round_rectangle(self, 0, 0, w, h, radius=radius, fill=bg, outline="")
        self.create_text(w/2, h/2, text=text, font=font, fill=fg)
        # bind
        if command:
            self.bind("<Button-1>", lambda e: command())

# ––– File I/O –––
CURR_FILE = "Asset/curriculum.txt"
def save_curriculum(data):
    os.makedirs(os.path.dirname(CURR_FILE), exist_ok=True)
    with open(CURR_FILE, 'w', encoding="utf-8") as f:
        for crit, desc in data:
            f.write(f"{crit}||{desc}\n")

def load_curriculum():
    if not os.path.exists(CURR_FILE):
        return []
    data = []
    with open(CURR_FILE, 'r', encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('||')
            if len(parts)==2:
                data.append((parts[0], parts[1]))
    return data

# ––– Curriculum Window –––
def open_curriculum_window():
    win = tk.Tk()
    win.title("Curriculum Management")
    win.configure(bg='white')
    win.geometry("900x500")

    data = load_curriculum()

    # Title
    tk.Label(win, text="Curriculum", font=("Arial",20,"bold"), bg="white").pack(pady=10)

    # Buttons
    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(pady=5)
    RoundButton(btn_frame, text="Add Curriculum", command=lambda: add_item(), bg="#A3C8F3").pack(side="left", padx=10)
    RoundButton(btn_frame, text="Back to Dashboard", command=lambda: back_to_dashboard(win), bg="#F3A3A3").pack(side="left", padx=10)

    # Scrollable area
    container = tk.Frame(win, bg="white")
    container.pack(fill="both", expand=True, padx=20, pady=(0,20))

    canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    vsb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    vsb.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=vsb.set)

    table_frame = tk.Frame(canvas, bg="white", bd=2, relief="solid")
    canvas.create_window((0,0), window=table_frame, anchor="nw")

    def on_frame_config(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
    table_frame.bind("<Configure>", on_frame_config)

    # Headers
    headers = ["#","Criteria","Description","Edit","Delete"]
    for i,h in enumerate(headers):
        tk.Label(table_frame, text=h, font=("Arial",10,"bold"), borderwidth=1, relief="solid", bg="#E0E0E0").grid(row=0, column=i, sticky="nsew")
    # column proportions: total weight 19 → 1,7,7,2,2
    for idx, w in enumerate([1,7,7,2,2]):
        table_frame.grid_columnconfigure(idx, weight=w)

    def refresh():
        # clear old
        for w in table_frame.winfo_children():
            info = w.grid_info()
            if info["row"] > 0:
                w.destroy()
        # repopulate
        for idx, (c, d) in enumerate(data):
            tk.Label(table_frame, text=str(idx + 1), borderwidth=1, relief="solid", bg="white", anchor="center").grid(row=idx + 1, column=0, sticky="nsew")
            tk.Label(table_frame, text=c, borderwidth=1, relief="solid", bg="white", anchor="w", padx=5).grid(row=idx + 1, column=1, sticky="nsew")
            tk.Label(table_frame, text=d, borderwidth=1, relief="solid", bg="white", anchor="w", padx=5, wraplength=400, justify="left").grid(row=idx + 1, column=2, sticky="nsew")

            # Edit button (rounded)
            edit_canvas = tk.Canvas(table_frame, width=80, height=30, bg="white", highlightthickness=0)
            edit_canvas.grid(row=idx + 1, column=3, sticky="nsew", padx=5, pady=5)
            RoundButton(edit_canvas, text="Edit", command=lambda i=idx: edit_item(i), bg="#A3C8F3", font=("Arial", 9)).pack(expand=True)

            # Delete button (rounded)
            delete_canvas = tk.Canvas(table_frame, width=80, height=30, bg="white", highlightthickness=0)
            delete_canvas.grid(row=idx + 1, column=4, sticky="nsew", padx=5, pady=5)
            RoundButton(delete_canvas, text="Delete", command=lambda i=idx: delete_item(i), bg="#F3A3A3", font=("Arial", 9)).pack(expand=True)

    def open_editor(index=None):
        # index=None for Add, otherwise Edit existing
        editor = tk.Toplevel()
        editor.title("Edit Curriculum" if index is not None else "Add Curriculum")
        editor.geometry("400x400")
        editor.configure(bg="white")

        # Center the popup nicely
        editor.update_idletasks()
        w = 400
        h = 400
        x = (editor.winfo_screenwidth() // 2) - (w // 2)
        y = (editor.winfo_screenheight() // 2) - (h // 2)
        editor.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(editor, text="Criteria:", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 0))
        criteria_text = tk.Text(editor, height=3, width=40, bd=2, relief="solid")
        criteria_text.pack(pady=5)

        tk.Label(editor, text="Description:", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 0))
        description_text = tk.Text(editor, height=8, width=40, bd=2, relief="solid")
        description_text.pack(pady=5)

        if index is not None:
            # Pre-fill text if editing
            crit, desc = data[index]
            criteria_text.insert("1.0", crit)
            description_text.insert("1.0", desc)

        button_frame = tk.Frame(editor, bg="white")
        button_frame.pack(pady=10)

        def save_and_close():
            new_crit = criteria_text.get("1.0", "end-1c").strip()
            new_desc = description_text.get("1.0", "end-1c").strip()
            if new_crit and new_desc:
                if index is None:
                    data.append((new_crit, new_desc))
                else:
                    data[index] = (new_crit, new_desc)
                save_curriculum(data)
                refresh()
                editor.destroy()
            else:
                messagebox.showwarning("Input Error", "Both fields must be filled!")

        RoundButton(button_frame, text="Save", bg="#A3C8F3", font=("Arial", 10), command=save_and_close).pack(side="left", padx=10)
        RoundButton(button_frame, text="Cancel", bg="#F3A3A3", font=("Arial", 10), command=editor.destroy).pack(side="left", padx=10)

    def add_item():
        open_editor(index=None)

    def edit_item(i):
        open_editor(index=i)

    def delete_item(i):
        if messagebox.askyesno("Confirm","Delete this entry?"):
            data.pop(i)
            save_curriculum(data)
            refresh()

    # mousewheel scrolling (Windows)
    def _on_mousewheel(evt):
        canvas.yview_scroll(int(-1*(evt.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    refresh()
    win.mainloop()


# --- Student Data ---
STUDENT_FILE = "Asset/dataStudent.txt"

def save_student_data(data):
    os.makedirs(os.path.dirname(STUDENT_FILE), exist_ok=True)
    with open(STUDENT_FILE, 'w', encoding="utf-8") as f:
        for student in data:
            f.write(f"{student['name']}||{'||'.join(student['grades'])}\n")

def load_student_data():
    if not os.path.exists(STUDENT_FILE):
        return []
    data = []
    with open(STUDENT_FILE, 'r', encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split('||')
            if len(parts) >= 2:
                student = {
                    'name': parts[0],
                    'grades': parts[1:]
                }
                data.append(student)
    return data

def open_student_grading_window():
    win = tk.Toplevel()
    win.title("Student Grading Management")
    win.geometry("800x600")
    win.configure(bg="white")

    data = load_student_data()
    criteria_list = [c for c, _ in load_curriculum()]  # Load criteria names dynamically

    # Title
    tk.Label(win, text="Grade Students", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

    # Top Buttons
    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(pady=5)

    RoundButton(btn_frame, text="Add Student", command=lambda: add_student(), bg="#A3C8F3").pack(side="left", padx=10)
    RoundButton(btn_frame, text="Back to Dashboard", command=lambda: back_to_dashboard(win), bg="#F3A3A3").pack(side="left", padx=10)
    RoundButton(btn_frame, text="Print Reports", command=lambda: print_reports(), bg="#A3F3A3").pack(side="left", padx=10)

    # Scrollable table area
    container = tk.Frame(win, bg="white")
    container.pack(fill="both", expand=True, padx=50, pady=(0, 20))

    tk_canvas = tk.Canvas(container, bg="white", highlightthickness=0)
    tk_canvas.pack(side="left", fill="both", expand=True)

    vsb = tk.Scrollbar(container, orient="vertical", command=tk_canvas.yview)
    vsb.pack(side="right", fill="y")

    tk_canvas.configure(yscrollcommand=vsb.set)

    # Create a frame inside the canvas to center contents
    canvas_frame = tk.Frame(tk_canvas, bg="white")
    tk_canvas.create_window((0, 0), window=canvas_frame, anchor="n")  # anchor "n" centers horizontally

    table_frame = tk.Frame(canvas_frame, bg="white", bd=2, relief="solid")
    table_frame.pack(pady=10)  # Center the table frame

    # Scrollregion update
    def on_frame_config(e):
        tk_canvas.configure(scrollregion=tk_canvas.bbox("all"))

    canvas_frame.bind("<Configure>", on_frame_config)

    # Table headers
    headers = ["#", "Student Name", "Grades", "Edit", "Delete"]
    for i, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", bg="#E0E0E0").grid(row=0, column=i, sticky="nsew")

    for idx in range(len(headers)):
        table_frame.grid_columnconfigure(idx, weight=1)

    # Refresh table
    def refresh():
        for w in table_frame.winfo_children():
            info = w.grid_info()
            if info["row"] > 0:
                w.destroy()

        for idx, student in enumerate(data):
            tk.Label(table_frame, text=str(idx + 1), borderwidth=1, relief="solid", bg="white", anchor="center").grid(row=idx + 1, column=0, sticky="nsew")

            tk.Label(table_frame, text=student['name'], borderwidth=1, relief="solid", bg="white", anchor="w", padx=5).grid(row=idx + 1, column=1, sticky="nsew")

            # Combine grades into a single column
            grades_text = ""
            for jdx, crit in enumerate(criteria_list):
                grade = student['grades'][jdx] if jdx < len(student['grades']) else "-"
                grades_text += f"{jdx+1}. {crit}: {grade}\n"

            tk.Label(table_frame, text=grades_text.strip(), borderwidth=1, relief="solid", bg="white", anchor="w", padx=5, justify="left", wraplength=400).grid(row=idx + 1, column=2, sticky="nsew")

            # Edit and Delete Buttons
            edit_canvas = tk.Canvas(table_frame, width=80, height=30, bg="white", highlightthickness=0)
            edit_canvas.grid(row=idx + 1, column=3, sticky="nsew", padx=5, pady=5)
            RoundButton(edit_canvas, text="Edit", command=lambda i=idx: edit_student(i), bg="#A3C8F3", font=("Arial", 9)).pack(expand=True)

            delete_canvas = tk.Canvas(table_frame, width=80, height=30, bg="white", highlightthickness=0)
            delete_canvas.grid(row=idx + 1, column=4, sticky="nsew", padx=5, pady=5)
            RoundButton(delete_canvas, text="Delete", command=lambda i=idx: delete_student(i), bg="#F3A3A3", font=("Arial", 9)).pack(expand=True)

    # Add, Edit, Delete Student Functions
    def add_student():
        editor = tk.Toplevel()
        editor.title("Add Student")
        editor.geometry("400x600")
        editor.configure(bg="white")

        tk.Label(editor, text="Student Name:", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 0))
        name_entry = tk.Entry(editor, width=40, bd=2, relief="solid")
        name_entry.pack(pady=5)

        grade_vars = {}
        for crit in criteria_list:
            frame = tk.Frame(editor, bg="white")
            frame.pack(pady=5, padx=10, anchor="w")

            tk.Label(frame, text=crit + ":", font=("Arial", 10), bg="white").pack(side="left")
            var = tk.StringVar(value="A+")
            dropdown = tk.OptionMenu(frame, var, "A+", "A", "B+", "B")
            dropdown.config(width=5)
            dropdown.pack(side="left", padx=10)
            grade_vars[crit] = var

        button_frame = tk.Frame(editor, bg="white")
        button_frame.pack(pady=10)

        def save_and_close():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Input Error", "Student name is required!")
                return

            grades = [grade_vars[c].get() for c in criteria_list]
            data.append({'name': name, 'grades': grades})
            save_student_data(data)
            refresh()
            editor.destroy()

        RoundButton(button_frame, text="Save", bg="#A3C8F3", font=("Arial", 10), command=save_and_close).pack(side="left", padx=10)
        RoundButton(button_frame, text="Cancel", bg="#F3A3A3", font=("Arial", 10), command=editor.destroy).pack(side="left", padx=10)

    def edit_student(index):
        student = data[index]

        editor = tk.Toplevel()
        editor.title("Edit Student")
        editor.geometry("400x600")
        editor.configure(bg="white")

        tk.Label(editor, text="Student Name:", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 0))
        name_entry = tk.Entry(editor, width=40, bd=2, relief="solid")
        name_entry.pack(pady=5)
        name_entry.insert(0, student['name'])

        grade_vars = {}
        for idx, crit in enumerate(criteria_list):
            frame = tk.Frame(editor, bg="white")
            frame.pack(pady=5, padx=10, anchor="w")

            tk.Label(frame, text=crit + ":", font=("Arial", 10), bg="white").pack(side="left")
            var = tk.StringVar(value=student['grades'][idx] if idx < len(student['grades']) else "A+")
            dropdown = tk.OptionMenu(frame, var, "A+", "A", "B+", "B")
            dropdown.config(width=5)
            dropdown.pack(side="left", padx=10)
            grade_vars[crit] = var

        button_frame = tk.Frame(editor, bg="white")
        button_frame.pack(pady=10)

        def save_and_close():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Input Error", "Student name is required!")
                return

            grades = [grade_vars[c].get() for c in criteria_list]
            data[index] = {'name': name, 'grades': grades}
            save_student_data(data)
            refresh()
            editor.destroy()

        RoundButton(button_frame, text="Save", bg="#A3C8F3", font=("Arial", 10), command=save_and_close).pack(side="left", padx=10)
        RoundButton(button_frame, text="Cancel", bg="#F3A3A3", font=("Arial", 10), command=editor.destroy).pack(side="left", padx=10)

    def delete_student(index):
        if messagebox.askyesno("Confirm", "Delete this student?"):
            data.pop(index)
            save_student_data(data)
            refresh()

    def print_reports():
        students = load_student_data()
        curriculum = load_curriculum()
        criteria_list = [c for c, _ in curriculum]

        if not students:
            messagebox.showinfo("No Data", "No student data to print.")
            return

        os.makedirs("Reports", exist_ok=True)

        for student in students:
            filename = f"Reports/{student['name'].replace(' ', '_')}_Report.pdf"
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4

            # Header
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, height - 50, "Hilmi Course")
            c.setFont("Helvetica", 14)
            c.drawString(50, height - 90, "STUDENT REPORT")

            # Info
            c.setFont("Helvetica", 11)
            c.drawString(50, height - 130, f"Student Name : {student['name']}")
            c.drawString(50, height - 150, "Academic Year : 2023 - 2024")
            c.drawString(50, height - 170, "Period       : March - August")
            c.drawString(50, height - 190, "Teacher Name : Mr. Ahmad Yazid")

            # Grades
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 230, "CLASSIFICATION")
            y = height - 260
            c.setFont("Helvetica", 11)
            for idx, criterion in enumerate(criteria_list):
                c.drawString(60, y, f"{idx + 1}. {criterion}")
                grade = student['grades'][idx] if idx < len(student['grades']) else "-"
                c.drawString(450, y, grade)
                y -= 20

            # Comment
            y -= 30
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "COMMENT")
            y -= 20
            c.setFont("Helvetica", 10)
            text = c.beginText(50, y)
            text.setLeading(14)
            comment = f"{student['name']} has shown great performance throughout the course. Keep improving and exploring new challenges!"
            text.textLines(comment)
            c.drawText(text)

            # Footer
            c.setFont("Helvetica", 9)
            c.drawString(50, 50, "A+ = Outstanding   A = Excellent   B+ = Good   B = Satisfactory")

            c.save()

        with open(STUDENT_FILE, 'w', encoding='utf-8') as f:
            f.write("")

        messagebox.showinfo("Done", "PDF reports generated in 'Reports/' folder.\nStudent data has been reset.")
        refresh()
        back_to_dashboard(win)

    # Mousewheel scrolling
    def _on_mousewheel(evt):
        tk_canvas.yview_scroll(int(-1 * (evt.delta / 120)), "units")
    tk_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    refresh()
    win.mainloop()



def back_to_dashboard(win):
    win.destroy()
    root.deiconify()



# ––– Your original Dashboard –––
def main_dashboard():
    global root, photo, img

    if not tk._default_root:
        root = tk.Tk()
        root.title("Teacher Grading Management")
        root.geometry("365x260")
        root.configure(bg='white')

        tk.Label(root, text="Teacher Grading Management", font=("Arial",12), bg="white").pack(pady=(5,0))

        c = tk.Canvas(root, width=365, height=220, bg='white', highlightthickness=0)
        c.pack()

        img = Image.open("Asset/imgs.png")
        img = img.resize((210,240))
        photo = ImageTk.PhotoImage(img)
        c.create_image(120,140, image=photo)

        def create_button(x, y, text, cmd):
            r = round_rectangle(c, x, y, x+120, y+35, radius=8, fill="#A3C8F3", outline="")
            lbl = c.create_text(x+60, y+18, text=text, font=("Arial",10), fill="black")
            c.tag_bind(r, "<Button-1>", lambda e: (root.withdraw(), cmd()))
            c.tag_bind(lbl, "<Button-1>", lambda e: (root.withdraw(), cmd()))

        create_button(220, 70, "Curriculum", open_curriculum_window)
        create_button(220, 130, "Grade Student", open_student_grading_window)

        root.mainloop()
    else:
        root.deiconify()




# ––– start here –––
main_dashboard()
