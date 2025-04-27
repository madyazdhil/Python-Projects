# Teacher Grading Report 📋✨

Welcome to the **Teacher Grading Report** project!

This project was born out of a real-life need: I needed to quickly create **student reports** in a short amount of time for many students — without doing everything manually.  
So I started exploring ways to make it easier using **Python** and **Tkinter**!

---

## 🚀 Features

- Create and manage **grading criteria** easily.
- Add, edit, and manage **student records** with their grades.
- **Automatically generate PDF reports** for each student (using ReportLab).
- Nice and simple **Tkinter GUI**, with custom **rounded buttons** and a modern look.
- Save and load data for curriculum and students automatically.
- Reset data after generating reports.

---

## 🛠️ Tech Stack

- Python 3
- Tkinter (for GUI)
- ReportLab (for PDF generation)
- PIL/Pillow (for image handling)

---

## 📂 Project Structure

```bash
Teacher Grading Report/
│
├── Asset/
│   ├── curriculum.txt         # Curriculum (grading criteria) saved here
│   ├── dataStudent.txt         # Student data saved here
│   └── imgs.png                # Image asset used in dashboard
│
├── Reports/                    # Generated PDF reports will be saved here
│   └── *.pdf
│
├── main.py                     # Main application file
└── .venv/                       # Python virtual environment (optional)
```

---

## 🧠 How It Works

- First, set up the **curriculum** (grading criteria).
- Then, **add students** and grade them based on the criteria.
- Finally, **generate PDF reports** for all students at once.
- After printing, student data resets to prepare for the next batch!

---

## 💡 Inspiration

As a teacher, I often faced situations where I had very **limited time** but needed to produce **professional reports** for **many students**.  
This tool made it **fast**, **organized**, and even **fun**!

---

## 🏗️ Future Improvements

- Add student photos to reports.
- Customizable grading scales (like A+, A, B+, etc.).
- Allow exporting student list to Excel/CSV.

---

## 🤝 Contributing

Feel free to explore, use, or suggest improvements!  
Pull requests and feedback are very welcome.
