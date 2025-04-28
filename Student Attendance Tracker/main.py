import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import os

# Class data file
DATA_FILE = 'Assets/class_data.txt'

# Load data function
def load_class_data():
    classes = []
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split("|")
                if len(parts) == 7:  # Now 7 fields
                    day, time, students, age_group, module, lessons_amt, start_date = parts
                    students_list = students.split(",")
                    classes.append((day, time, students_list, age_group, module, lessons_amt, start_date))
    return classes


# Save class function
def save_class(day, time, students, age_group, module, lessons_amt, start_date, overwrite=False):
    if overwrite:
        with open(DATA_FILE, "w") as f:
            for cls in classes_data:
                students_str = ",".join(cls[2])
                f.write(f"{cls[0]}|{cls[1]}|{students_str}|{cls[3]}|{cls[4]}|{cls[5]}|{cls[6]}\n")
    else:
        with open(DATA_FILE, "a") as f:
            students_str = ",".join(students)
            f.write(f"{day}|{time}|{students_str}|{age_group}|{module}|{lessons_amt}|{start_date}\n")


# ----- Main Dashboard ----- #

## Functions
def open_classes_window():
    dashboard.withdraw()
    show_class_menu()

def open_presence_window():
    dashboard.withdraw()
    show_presence_menu()

## Designs
def show_main_dashboard():
    global dashboard
    dashboard = tk.Tk()
    dashboard.title("Student & Class Tracker")
    dashboard.geometry("365x260")
    dashboard.configure(bg='#FBE4E4')

    # Title
    tk.Label(dashboard, text="Student & Class Tracker", font=("Arial", 16, "bold"), bg="#FBE4E4").pack(pady=(10, 0))
    tk.Label(dashboard, text="Mr. Ahmad Yazid", font=("Arial", 10), bg="#FBE4E4").pack()

    # Buttons
    buttons_frame = tk.Frame(dashboard, bg="#FBE4E4")
    buttons_frame.pack(pady=30)

    # Rectangle + Button for Classes
    class_canvas = tk.Canvas(buttons_frame, width=120, height=70, bg="#FBE4E4", highlightthickness=0)
    class_canvas.grid(row=0, column=0, padx=10)
    class_canvas.create_rectangle(0, 10, 120, 60, fill="#FFAFAF", outline="")
    class_button = tk.Button(buttons_frame, text="Classes", bg="#FF6262", command=open_classes_window, bd=0)
    class_canvas.create_window(60, 35, window=class_button)

    # Rectangle + Button for Presence
    presence_canvas = tk.Canvas(buttons_frame, width=120, height=70, bg="#FBE4E4", highlightthickness=0)
    presence_canvas.grid(row=0, column=1, padx=10)
    presence_canvas.create_rectangle(0, 10, 120, 60, fill="#FFD4D4", outline="")
    presence_button = tk.Button(buttons_frame, text="Presence", bg="#FF6262", bd=0, command=open_presence_window)
    presence_canvas.create_window(60, 35, window=presence_button)

    # Date
    today = datetime.now().strftime("%A, %d-%b-%Y")
    tk.Label(dashboard, text=today, font=("Arial", 9), bg="#FBE4E4").pack(side="bottom", pady=10)


# ----- Presence Dashboard ----- #

## Functions
def show_presence_menu():
    presence_window = tk.Toplevel()
    presence_window.configure(bg='#FBE4E4')
    presence_window.geometry('400x200')
    presence_window.title("Presence Dashboard")

    tk.Label(presence_window, text="Presence Tracking Coming Soon", bg="#FBE4E4", font=("Arial", 16)).pack(expand=True)

    tk.Button(presence_window, text="Back", command=lambda: (presence_window.destroy(), dashboard.deiconify())).pack(pady=10)

## Designs
# (coming soon)


# ----- Class Menu ----- #

## Functions
def show_class_menu():
    global class_window, table_canvas, table_frame, scrollbar
    classes = load_class_data()

    class_window = tk.Toplevel()
    class_window.configure(bg='#FBE4E4')
    class_window.geometry('800x500')
    class_window.title("Class List")

    # Title
    tk.Label(class_window, text="Class List", font=("Arial", 16, "bold"), bg="#FBE4E4").pack(pady=(10, 0))
    tk.Label(class_window, text="Mr. Ahmad Yazid", font=("Arial", 10), bg="#FBE4E4").pack()

    # Buttons
    button_frame = tk.Frame(class_window, bg="#FBE4E4")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Class", bg="#D6F0FF", command=open_add_class_window).grid(row=0, column=0,
                                                                                                padx=10)
    tk.Button(button_frame, text="Dashboard", bg="#FFE4B5",
              command=lambda: (class_window.destroy(), dashboard.deiconify())).grid(row=0, column=1, padx=10)

    # Scrollable Table Frame
    container = tk.Frame(class_window, bg="#FBE4E4")
    container.pack(fill="both", expand=True, pady=10)

    table_canvas = tk.Canvas(container, bg="#FBE4E4", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=table_canvas.yview)

    scrollable_frame = tk.Frame(table_canvas, bg="#FBE4E4")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: table_canvas.configure(
            scrollregion=table_canvas.bbox("all"),
            width=800
        )
    )

    table_canvas.create_window((400, 0), window=scrollable_frame, anchor="n")  # <-- Centering horizontally
    table_canvas.configure(yscrollcommand=scrollbar.set)

    table_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    table_frame = scrollable_frame

    # Make mousewheel work
    def _on_mousewheel(event):
        table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    table_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    show_classes()


def show_classes():
    for widget in table_frame.winfo_children():
        widget.destroy()

    headers = ["#", "Day", "Time", "Students", "Action"]
    for i, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=("Arial", 10, "bold"), bg="#FBE4E4").grid(row=0, column=i, padx=15, pady=10)

    global classes_data
    classes_data = load_class_data()

    for idx, (day, time, students, age_group, module, lessons_amt, start_date) in enumerate(classes_data, start=1):
        tk.Label(table_frame, text=idx, bg="#FBE4E4").grid(row=idx, column=0, padx=10, pady=10)
        tk.Label(table_frame, text=day, bg="#FBE4E4").grid(row=idx, column=1, padx=10, pady=10)
        tk.Label(table_frame, text=time, bg="#FBE4E4").grid(row=idx, column=2, padx=10, pady=10)
        tk.Label(table_frame, text="\n".join(students), justify="left", bg="#FBE4E4").grid(row=idx, column=3, padx=10, pady=10)

        action_frame = tk.Frame(table_frame, bg="#FBE4E4")
        action_frame.grid(row=idx, column=4, padx=10, pady=10)

        tk.Button(action_frame, text="Edit", width=6, height=1, command=lambda i=idx-1: open_edit_class_window(i)).pack(side="top", pady=2)
        tk.Button(action_frame, text="Delete", width=6, height=1, command=lambda i=idx-1: delete_class(i)).pack(side="top", pady=2)



def open_add_class_window():
    add_class_window = tk.Toplevel()
    add_class_window.configure(bg='#FBE4E4')
    add_class_window.geometry('650x400')
    add_class_window.title("Add Class")

    tk.Label(add_class_window, text="Add Class", font=("Arial", 16, "bold"), bg="#FBE4E4").pack(pady=10)

    form_frame = tk.Frame(add_class_window, bg="#FBE4E4")
    form_frame.pack(pady=10)

    # Day
    tk.Label(form_frame, text="Day", bg="#FBE4E4").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    day_combo = ttk.Combobox(form_frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], width=10)
    day_combo.grid(row=0, column=1, pady=5, padx=5)

    # Age Group
    tk.Label(form_frame, text="Age Group", bg="#FBE4E4").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    age_combo = ttk.Combobox(form_frame, values=["Kids", "Teens"], width=10)
    age_combo.grid(row=0, column=3, pady=5, padx=5)

    # Module
    tk.Label(form_frame, text="Module", bg="#FBE4E4").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    module_combo = ttk.Combobox(form_frame, values=["Python", "Web", "Robot", "Roblox"], width=10)
    module_combo.grid(row=1, column=1, pady=5, padx=5)

    # Predefined Session
    tk.Label(form_frame, text="Session", bg="#FBE4E4").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    session_combo = ttk.Combobox(form_frame, width=20, values=[
        "10:00 - 11:00",
        "11:00 - 12:00",
        "12:00 - 13:00",
        "13:00 - 14:00",
        "14:00 - 15:00",
        "15:00 - 16:00",
        "10:00 - 11:30",
        "11:30 - 13:00",
        "13:00 - 14:30",
        "14:30 - 16:00"
    ])
    session_combo.grid(row=2, column=1, pady=5, padx=5)

    # Non-session (custom time)
    tk.Label(form_frame, text="Non-Session", bg="#FBE4E4").grid(row=2, column=2, sticky="w", padx=5, pady=5)

    non_session_frame = tk.Frame(form_frame, bg="#FBE4E4")
    non_session_frame.grid(row=2, column=3, pady=5)

    # Start time
    start_hour = ttk.Combobox(non_session_frame, width=3, values=[f"{h:02d}" for h in range(9, 21)])
    start_hour.grid(row=0, column=0)
    tk.Label(non_session_frame, text=":", bg="#FBE4E4").grid(row=0, column=1)
    start_minute = ttk.Combobox(non_session_frame, width=3, values=["00", "15", "30", "45"])
    start_minute.grid(row=0, column=2)

    # "to" label
    tk.Label(non_session_frame, text="to", bg="#FBE4E4").grid(row=0, column=3, padx=(10, 10))

    # End time
    end_hour = ttk.Combobox(non_session_frame, width=3, values=[f"{h:02d}" for h in range(9, 21)])
    end_hour.grid(row=0, column=4)
    tk.Label(non_session_frame, text=":", bg="#FBE4E4").grid(row=0, column=5)
    end_minute = ttk.Combobox(non_session_frame, width=3, values=["00", "15", "30", "45"])
    end_minute.grid(row=0, column=6)

    # Students
    tk.Label(form_frame, text="Students", bg="#FBE4E4").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
    students_entry = tk.Text(form_frame, width=40, height=5)
    students_entry.grid(row=3, column=1, columnspan=3, pady=5, padx=5)

    # Lessons Amt
    tk.Label(form_frame, text="Lessons Amt", bg="#FBE4E4").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    lesson_combo = ttk.Combobox(form_frame, values=[10, 15, 20], width=10)
    lesson_combo.grid(row=4, column=1, pady=5, padx=5)

    # Start Date
    tk.Label(form_frame, text="Start Date", bg="#FBE4E4").grid(row=4, column=2, sticky="w", padx=5, pady=5)
    start_date = DateEntry(form_frame, date_pattern='dd-mm-yyyy')
    start_date.grid(row=4, column=3, pady=5, padx=5)

    # Save and Cancel
    button_frame = tk.Frame(add_class_window, bg="#FBE4E4")
    button_frame.pack(pady=20)

    def save_new_class():
        day = day_combo.get()
        age = age_combo.get()
        module = module_combo.get()

        session = session_combo.get()
        if not session:
            start = f"{start_hour.get()}:{start_minute.get()}"
            end = f"{end_hour.get()}:{end_minute.get()}"
            session = f"{start} - {end}"

        students = students_entry.get("1.0", "end-1c").split(",")
        students = [s.strip() for s in students if s.strip() != ""]

        lesson_amt = lesson_combo.get()
        start_dt = start_date.get()

        save_class(day, session, students, age, module, lesson_amt, start_dt)

        add_class_window.destroy()
        show_classes()

    tk.Button(button_frame, text="Save", bg="#C2F0C2", width=10, command=save_new_class).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", bg="#FFB6B6", width=10, command=add_class_window.destroy).pack(side="left", padx=10)



def open_edit_class_window(index):
    add_class_window = tk.Toplevel()
    add_class_window.configure(bg='#FBE4E4')
    add_class_window.geometry('650x400')
    add_class_window.title("Edit Class")

    tk.Label(add_class_window, text="Edit Class", font=("Arial", 16, "bold"), bg="#FBE4E4").pack(pady=10)

    form_frame = tk.Frame(add_class_window, bg="#FBE4E4")
    form_frame.pack(pady=10)

    # Day
    tk.Label(form_frame, text="Day", bg="#FBE4E4").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    day_combo = ttk.Combobox(form_frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], width=10)
    day_combo.grid(row=0, column=1, pady=5, padx=5)

    # Age Group
    tk.Label(form_frame, text="Age Group", bg="#FBE4E4").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    age_combo = ttk.Combobox(form_frame, values=["Kids", "Teens"], width=10)
    age_combo.grid(row=0, column=3, pady=5, padx=5)

    # Module
    tk.Label(form_frame, text="Module", bg="#FBE4E4").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    module_combo = ttk.Combobox(form_frame, values=["Python", "Web", "Robot", "Roblox"], width=10)
    module_combo.grid(row=1, column=1, pady=5, padx=5)

    # Session
    tk.Label(form_frame, text="Session", bg="#FBE4E4").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    session_combo = ttk.Combobox(form_frame, width=20, values=[
        "10:00 - 11:00",
        "11:00 - 12:00",
        "12:00 - 13:00",
        "13:00 - 14:00",
        "14:00 - 15:00",
        "15:00 - 16:00",
        "10:00 - 11:30",
        "11:30 - 13:00",
        "13:00 - 14:30",
        "14:30 - 16:00"
    ])
    session_combo.grid(row=2, column=1, pady=5, padx=5)

    # Non-session (custom time)
    tk.Label(form_frame, text="Non-Session", bg="#FBE4E4").grid(row=2, column=2, sticky="w", padx=5, pady=5)

    non_session_frame = tk.Frame(form_frame, bg="#FBE4E4")
    non_session_frame.grid(row=2, column=3, pady=5)

    # Start time
    start_hour = ttk.Combobox(non_session_frame, width=3, values=[f"{h:02d}" for h in range(9, 21)])
    start_hour.grid(row=0, column=0)
    tk.Label(non_session_frame, text=":", bg="#FBE4E4").grid(row=0, column=1)
    start_minute = ttk.Combobox(non_session_frame, width=3, values=["00", "15", "30", "45"])
    start_minute.grid(row=0, column=2)

    # "to" label
    tk.Label(non_session_frame, text="to", bg="#FBE4E4").grid(row=0, column=3, padx=(10, 10))

    # End time
    end_hour = ttk.Combobox(non_session_frame, width=3, values=[f"{h:02d}" for h in range(9, 21)])
    end_hour.grid(row=0, column=4)
    tk.Label(non_session_frame, text=":", bg="#FBE4E4").grid(row=0, column=5)
    end_minute = ttk.Combobox(non_session_frame, width=3, values=["00", "15", "30", "45"])
    end_minute.grid(row=0, column=6)


    # Students
    tk.Label(form_frame, text="Students", bg="#FBE4E4").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
    students_entry = tk.Text(form_frame, width=40, height=5)
    students_entry.grid(row=3, column=1, columnspan=3, pady=5, padx=5)

    # Lessons Amt
    tk.Label(form_frame, text="Lessons Amt", bg="#FBE4E4").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    lesson_combo = ttk.Combobox(form_frame, values=[10, 15, 20], width=10)
    lesson_combo.grid(row=4, column=1, pady=5, padx=5)

    # Start Date
    tk.Label(form_frame, text="Start Date", bg="#FBE4E4").grid(row=4, column=2, sticky="w", padx=5, pady=5)
    start_date = DateEntry(form_frame, date_pattern='dd-mm-yyyy')
    start_date.grid(row=4, column=3, pady=5, padx=5)

    # Pre-fill data
    if index is not None:
        day_combo.set(classes_data[index][0])
        session_combo.set(classes_data[index][1])
        students_entry.insert("1.0", ", ".join(classes_data[index][2]))
        age_combo.set(classes_data[index][3])
        module_combo.set(classes_data[index][4])
        lesson_combo.set(classes_data[index][5])
        start_date.set_date(classes_data[index][6])

    # Save and Cancel
    button_frame = tk.Frame(add_class_window, bg="#FBE4E4")
    button_frame.pack(pady=20)

    def save_action():
        day = day_combo.get()
        age = age_combo.get()
        module = module_combo.get()

        session = session_combo.get()
        if not session:  # If no session selected, use non-session manual input
            start = f"{start_hour.get()}:{start_minute.get()}"
            end = f"{end_hour.get()}:{end_minute.get()}"
            session = f"{start} - {end}"

        students = students_entry.get("1.0", "end-1c").split(",")
        students = [s.strip() for s in students if s.strip() != ""]

        lesson_amt = lesson_combo.get()
        start_dt = start_date.get()

        if index is not None:
            classes_data[index] = (day, session, students, age, module, lesson_amt, start_dt)
            save_class(day, session, students, age, module, lesson_amt, start_dt, overwrite=True)

        add_class_window.destroy()
        show_classes()

    tk.Button(button_frame, text="Save", bg="#C2F0C2", width=10, command=save_action).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", bg="#FFB6B6", width=10, command=add_class_window.destroy).pack(side="left", padx=10)



def delete_class(index):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this class?"):
        del classes_data[index]
        save_class(None, None, None, overwrite=True)
        show_classes()

# ----- Presence Dashboard ----- #


# Mapping days to sort properly
day_order = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}


def sort_classes(classes):
    def sort_key(cls):
        day, time, *_ = cls
        start_time = time.split('-')[0].strip()
        start_hour, start_minute = map(int, start_time.split(":"))
        return (day_order.get(day, 8), start_hour, start_minute)

    return sorted(classes, key=sort_key)


def show_presence_menu():
    global presence_window, presence_table_frame, presence_canvas, presence_scrollbar

    classes = load_class_data()
    sorted_classes = sort_classes(classes)

    presence_window = tk.Toplevel()
    presence_window.configure(bg='#FBE4E4')
    presence_window.geometry('800x500')
    presence_window.title("Presence Dashboard")

    # Title
    tk.Label(presence_window, text="Student Absent", font=("Arial", 18, "bold"), bg="#FBE4E4").pack(pady=(10, 0))
    tk.Label(presence_window, text="Mr. Ahmad Yazid", font=("Arial", 10), bg="#FBE4E4").pack()

    today = datetime.now().strftime("%A, %d-%b-%Y")
    tk.Label(presence_window, text=today, font=("Arial", 9), bg="#FBE4E4").pack()

    # Dashboard Button
    tk.Button(presence_window, text="Dashboard", bg="#FFE4B5",
              command=lambda: (presence_window.destroy(), dashboard.deiconify())).pack(pady=10)

    # Scrollable Table Frame
    container = tk.Frame(presence_window, bg="#FBE4E4")
    container.pack(fill="both", expand=True, pady=10)

    presence_canvas = tk.Canvas(container, bg="#FBE4E4", highlightthickness=0)
    presence_scrollbar = tk.Scrollbar(container, orient="vertical", command=presence_canvas.yview)

    scrollable_frame = tk.Frame(presence_canvas, bg="#FBE4E4")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: presence_canvas.configure(
            scrollregion=presence_canvas.bbox("all"),
            width=800
        )
    )

    presence_canvas.create_window((400, 0), window=scrollable_frame, anchor="n")
    presence_canvas.configure(yscrollcommand=presence_scrollbar.set)

    presence_canvas.pack(side="left", fill="both", expand=True)
    presence_scrollbar.pack(side="right", fill="y")

    presence_table_frame = scrollable_frame

    # Enable Mousewheel
    def _on_mousewheel(event):
        presence_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    presence_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    show_presence_classes(sorted_classes)


def show_presence_classes(classes):
    for widget in presence_table_frame.winfo_children():
        widget.destroy()

    headers = ["#", "Day", "Time", "Students", "Action"]
    for i, h in enumerate(headers):
        tk.Label(presence_table_frame, text=h, font=("Arial", 10, "bold"), bg="#FBE4E4").grid(row=0, column=i, padx=15,
                                                                                              pady=10)

    for idx, (day, time, students, *_rest) in enumerate(classes, start=1):
        tk.Label(presence_table_frame, text=idx, bg="#FBE4E4").grid(row=idx, column=0, padx=10, pady=10)
        tk.Label(presence_table_frame, text=day, bg="#FBE4E4").grid(row=idx, column=1, padx=10, pady=10)
        tk.Label(presence_table_frame, text=time, bg="#FBE4E4").grid(row=idx, column=2, padx=10, pady=10)
        tk.Label(presence_table_frame, text="\n".join(students), justify="left", bg="#FBE4E4").grid(row=idx, column=3,
                                                                                                    padx=10, pady=10)

        action_frame = tk.Frame(presence_table_frame, bg="#FBE4E4")
        action_frame.grid(row=idx, column=4, padx=10, pady=10)

        tk.Button(action_frame, text="Absent", width=8, command=lambda d=day, t=time: mark_absent(d, t)).pack()


def mark_absent(day, time):
    classes = load_class_data()
    selected_class = None
    for cls in classes:
        if cls[0] == day and cls[1] == time:
            selected_class = cls
            break

    if not selected_class:
        messagebox.showerror("Error", "Class not found!")
        return

    # Extract class data
    day, time, students, age_group, module, lessons_amt, start_date = selected_class

    absent_window = tk.Toplevel()
    absent_window.title(f"Absent for Class {day} {time}")
    absent_window.geometry('600x500')
    absent_window.configure(bg='#FBE4E4')

    tk.Label(absent_window, text=f"Absent for Class {day} {time}", font=("Arial", 16, "bold"), bg="#FBE4E4").pack(pady=10)

    today = datetime.now().strftime("%A, %d-%b-%Y")
    tk.Label(absent_window, text=today, font=("Arial", 10), bg="#FBE4E4").pack()

    form_frame = tk.Frame(absent_window, bg="#FBE4E4")
    form_frame.pack(pady=10)

    # Class Status
    tk.Label(form_frame, text="Class Status", bg="#FBE4E4").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    class_status = ttk.Combobox(form_frame, values=["Complete", "Incomplete"], width=15)
    class_status.grid(row=0, column=1, pady=5, padx=5)
    class_status.set("Complete")

    # Lesson #
    tk.Label(form_frame, text="Lesson #", bg="#FBE4E4").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    lesson_numbers = [f"Lesson {i+1}" for i in range(int(lessons_amt))]
    lesson_combo = ttk.Combobox(form_frame, values=lesson_numbers, width=15)
    lesson_combo.grid(row=0, column=3, pady=5, padx=5)
    lesson_combo.set(lesson_numbers[0])

    # Table Headers
    headers = ["#", "Students", "Presence"]
    for i, h in enumerate(headers):
        tk.Label(form_frame, text=h, font=("Arial", 10, "bold"), bg="#FBE4E4").grid(row=1, column=i, padx=10, pady=10)

    presence_vars = []

    # Students List
    for idx, student in enumerate(students, start=1):
        tk.Label(form_frame, text=idx, bg="#FBE4E4").grid(row=idx+1, column=0, padx=10, pady=5)
        tk.Label(form_frame, text=student, bg="#FBE4E4").grid(row=idx+1, column=1, padx=10, pady=5)

        presence = ttk.Combobox(form_frame, values=["Present", "Absent"], width=10)
        presence.grid(row=idx+1, column=2, padx=10, pady=5)
        presence.set("Present")
        presence_vars.append((student, presence))

    # Comment Section
    tk.Label(absent_window, text="Class Comment", bg="#FBE4E4", font=("Arial", 10)).pack(pady=(20, 5))
    comment_box = tk.Text(absent_window, width=60, height=4)
    comment_box.pack()

    # Buttons
    button_frame = tk.Frame(absent_window, bg="#FBE4E4")
    button_frame.pack(pady=20)

    def save_absent():
        presence_data = []
        for student, presence_widget in presence_vars:
            status = presence_widget.get()
            presence_data.append(f"{student} = {status}")

        comment = comment_box.get("1.0", "end-1c").strip()

        # Save to absent_data.txt
        with open("Assets/absent_data.txt", "a") as f:
            f.write(f"{day}, {start_date}|{today}|{class_status.get()}|{lesson_combo.get()}|{' ; '.join(presence_data)}|{comment}\n")

        messagebox.showinfo("Saved", "Attendance record saved!")
        absent_window.destroy()

    tk.Button(button_frame, text="Save", bg="#C2F0C2", width=10, command=save_absent).pack(side="left", padx=10)
    tk.Button(button_frame, text="Cancel", bg="#FFB6B6", width=10, command=absent_window.destroy).pack(side="left", padx=10)



# ----- Window Management ----- #
show_main_dashboard()
dashboard.mainloop()
