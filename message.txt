import customtkinter
from PIL import Image
from tkinter import messagebox
import requests

MACHINE_B_URL = "http://192.168.56.3:5000/students"

def fade_in(window, step=0.05, delay=10):
    if not window.winfo_exists():
        return
    window.attributes("-alpha", 0)
    window.update()
    alpha = 0
    while alpha <= 1:
        if not window.winfo_exists():
            return
        window.attributes("-alpha", alpha)
        window.update()
        window.after(delay)
        alpha += step
    window.attributes("-alpha", 1)

def fade_out(window, step=0.05, delay=10):
    if not window.winfo_exists():
        return
    alpha = 1
    while alpha >= 0:
        if not window.winfo_exists():
            return
        window.attributes("-alpha", alpha)
        window.update()
        window.after(delay)
        alpha -= step
    window.attributes("-alpha", 0)

def destroy_previous(previous_window):
    if previous_window and previous_window.winfo_exists():
        fade_out(previous_window)
        previous_window.destroy()

def load_students():
    try:
        response = requests.get(MACHINE_B_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        for aluno in data:
            if "school_grades" not in aluno or not isinstance(aluno["school_grades"], dict):
                aluno["school_grades"] = {"AVA 1": 0.0, "AVA 2": 0.0, "AVA 3": 0.0}
            else:
                for n in ["AVA 1", "AVA 2", "AVA 3"]:
                    aluno["school_grades"].setdefault(n, 0.0)
        return data
    except requests.RequestException as e:
        messagebox.showerror("Erro", f"Não foi possível carregar os alunos da Máquina B: {e}")
        return []

def save_student(student):
    try:
        requests.post(f"{MACHINE_B_URL}/update", json=student, timeout=5)
    except requests.RequestException as e:
        messagebox.showerror("Erro", f"Não foi possível atualizar os dados na Máquina B: {e}")

def get_students_by_class(class_name):
    data = load_students()
    turma_key = class_name[-1]
    return [aluno for aluno in data if aluno.get("student_class", "").endswith(turma_key)]

def calculate_average(grades):
    try:
        return round((float(grades["AVA 1"]) + float(grades["AVA 2"]) + float(grades["AVA 3"])) / 3, 2)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0.0

def color_average(average):
    if average >= 7:
        return "green"
    elif average >= 5:
        return "#e6b800"
    else:
        return "red"

def open_student_details(student, refresh_callback, parent_window):
    details_win = customtkinter.CTkToplevel(parent_window)
    details_win.title(f"Detalhes - {student['name']}")
    details_win.geometry("420x520")
    details_win.resizable(False, False)
    details_win.transient(parent_window)
    details_win.grab_set()
    details_win.focus()

    customtkinter.CTkLabel(details_win, text="Informações do Aluno", font=("Arial Black", 18)).pack(pady=15)
    customtkinter.CTkLabel(details_win, text=f"Nome: {student['name']}", font=("Arial", 14)).pack(pady=5)
    customtkinter.CTkLabel(details_win, text=f"E-mail: {student['email']}", font=("Arial", 14)).pack(pady=5)
    customtkinter.CTkLabel(details_win, text=f"Turma: {student['student_class']}", font=("Arial", 14)).pack(pady=5)

    frame_average = customtkinter.CTkFrame(details_win, fg_color="#f2f2f2", corner_radius=10)
    frame_average.pack(pady=20, padx=20, fill="x")

    customtkinter.CTkLabel(frame_average, text="Notas:", font=("Arial Black", 14)).pack(pady=10)

    grade_vars = {}
    for n in ["AVA 1", "AVA 2", "AVA 3"]:
        average_frame = customtkinter.CTkFrame(frame_average, fg_color="#ffffff", corner_radius=8)
        average_frame.pack(pady=5, padx=10, fill="x")
        customtkinter.CTkLabel(average_frame, text=f"{n}:", font=("Arial", 13, "bold"), width=40).pack(side="left", padx=10)
        grade_vars[n] = customtkinter.StringVar(value=str(student["school_grades"].get(n, 0.0)))
        customtkinter.CTkEntry(average_frame, textvariable=grade_vars[n], width=80).pack(side="left", padx=10, pady=8)

    average_label = customtkinter.CTkLabel(details_win, text="", font=("Arial Black", 14))
    average_label.pack(pady=10)

    def refresh_average(*args):
        grades = {n: grade_vars[n].get() for n in ["AVA 1", "AVA 2", "AVA 3"]}
        try:
            average = calculate_average({k: float(v) for k, v in grades.items()})
        except ValueError:
            average = 0.0
        average_color = color_average(average)
        average_label.configure(text=f"Média atual: {average}", text_color=average_color)

    for var in grade_vars.values():
        var.trace_add("write", refresh_average)
    refresh_average()

    def save_grades():
        try:
            new_grades = {n: float(grade_vars[n].get()) for n in ["AVA 1", "AVA 2", "AVA 3"]}
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira apenas números válidos nas notas.")
            return
        student["school_grades"] = new_grades
        save_student(student)
        messagebox.showinfo("Sucesso", f"As notas de {student['name']} foram atualizadas.")
        details_win.destroy()
        refresh_callback()

    customtkinter.CTkButton(
        details_win, text="Salvar Notas", fg_color="#005f99",
        hover_color="#007acc", command=save_grades, width=160, height=35
    ).pack(pady=15)

    customtkinter.CTkButton(
        details_win, text="Fechar", fg_color="gray", hover_color="#444",
        command=details_win.destroy, width=100, height=30
    ).pack(pady=5)

def classes_window(previous_window):
    destroy_previous(previous_window)
    new_window = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}+0+0")
    new_window.attributes("-fullscreen", True)
    new_window.title("Minhas Classes")

    main_frame = customtkinter.CTkFrame(new_window, fg_color="#000000")
    main_frame.pack(fill="both", expand=True)

    header = customtkinter.CTkFrame(main_frame, fg_color="#6d7675", height=80, corner_radius=0)
    header.pack(fill="x", side="top")

    logo_image = customtkinter.CTkImage(dark_image=Image.open("assets/img/logo.png"), size=(40, 70))
    logo_button = customtkinter.CTkButton(
        header,
        text="BRISPACE",
        image=logo_image,
        compound="left",
        fg_color="transparent",
        hover_color="#6d7675",
        text_color="black",
        font=("Arial Black", 32),
        command=lambda: teacher_window({'name': 'Professor'}, new_window)
    )
    logo_button.pack(side="left", padx=40, pady=20)

    btn_exit = customtkinter.CTkButton(
        header,
        text="Sair",
        width=120,
        height=35,
        corner_radius=15,
        font=("Arial", 14, "bold"),
        fg_color="#000000",
        hover_color="#cfe2ff",
        text_color="white",
        command=lambda: fade_out(new_window) or new_window.destroy()
    )
    btn_exit.pack(side="right", padx=40)

    body = customtkinter.CTkFrame(main_frame, fg_color="#394440")
    body.pack(fill="both", expand=True, pady=(10, 0))

    sidebar = customtkinter.CTkFrame(body, width=250, fg_color="#ffffff", corner_radius=12)
    sidebar.pack(side="left", fill="y", padx=30, pady=30)
    sidebar_title = customtkinter.CTkLabel(sidebar, text="Turmas:", font=("Arial Bold", 18), text_color="black")
    sidebar_title.pack(pady=(15, 20))

    content_frame = customtkinter.CTkFrame(body, fg_color="white", corner_radius=16)
    content_frame.pack(side="right", fill="both", expand=True, padx=(10, 30), pady=30)

    content_icon = customtkinter.CTkLabel(content_frame, text="🏫", font=("Arial", 90))
    content_icon.pack(pady=(120, 20))

    content_label = customtkinter.CTkLabel(
        content_frame,
        text="Selecione uma turma ao lado para visualizar os alunos.",
        font=("Arial", 18),
        text_color="#333333"
    )
    content_label.pack()

    icon_path = "assets/teacher_window/class"
    def load_icon(filename, size=(30, 30)):
        from os import path
        img_path = path.join(icon_path, filename)
        return customtkinter.CTkImage(
            dark_image=Image.open(img_path),
            light_image=Image.open(img_path),
            size=size
        )

    student_icon = load_icon("student.png")

    def mostrar_turma(nome):
        for widget in content_frame.winfo_children():
            widget.destroy()
        
        alunos = get_students_by_class(nome)

        class_title = customtkinter.CTkLabel(
            content_frame,
            text=f"📘 {nome}",
            font=("Arial Black", 24),
            text_color="#000000"
        )
        class_title.pack(pady=(40, 20))

        students_frame = customtkinter.CTkScrollableFrame(content_frame, fg_color="#f5f6fa", width=600, height=400)
        students_frame.pack(pady=10, padx=40, fill="both", expand=True)

        if not alunos:
            empty_label = customtkinter.CTkLabel(
                students_frame,
                text="Nenhum aluno cadastrado nesta turma.",
                font=("Arial", 16),
                text_color="#555555"
            )
            empty_label.pack(pady=20)
            return

        for aluno in alunos:
            grades = aluno.get("school_grades", {"AVA 1": 0, "AVA 2": 0, "AVA 3": 0})
            average = calculate_average(grades)
            average_color = color_average(average)
            
            def open_details(a=aluno):
                open_student_details(a, lambda: mostrar_turma(nome), new_window)
            
            btn = customtkinter.CTkButton(
                students_frame,
                text=f"  {aluno['name']}  |  AVA 1: {grades['AVA 1']}  AVA 2: {grades['AVA 2']}  AVA 3: {grades['AVA 3']}  →  Média: {average}",
                image=student_icon,
                compound="left",
                anchor="w",
                width=600,
                height=60,
                corner_radius=10,
                font=("Arial", 16, "bold"),
                fg_color="white",
                text_color=average_color,
                border_color="#004aad",
                border_width=1,
                hover_color="#d0e3ff",
                command=open_details
            )
            btn.pack(pady=10, padx=40)

    for class_name in ["Turma A", "Turma B"]:
        class_btn = customtkinter.CTkButton(
            sidebar,
            text=class_name,
            font=("Arial", 16, "bold"),
            fg_color="#ffffff",
            text_color="black",
            hover_color="#cfe2ff",
            corner_radius=10,
            border_width=2,
            border_color="#004aad",
            command=lambda t=class_name: mostrar_turma(t)
        )
        class_btn.pack(fill="x", padx=15, pady=10)

    fade_in(new_window)

def teacher_window(user, previous_window=None):
    if previous_window:
        previous_window.destroy()
    window = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}+0+0")
    window.attributes("-fullscreen", True)
    window.title("Área do Professor")

    main_frame = customtkinter.CTkFrame(window, fg_color="#000000")
    main_frame.pack(fill="both", expand=True)

    header = customtkinter.CTkFrame(main_frame, fg_color="#6d7675", height=80, corner_radius=0)
    header.pack(fill="x", side="top")

    logo_image = customtkinter.CTkImage(dark_image=Image.open("assets/img/logo.png"), size=(40, 70))
    title_label = customtkinter.CTkLabel(
        header,
        text="BRISPACE",
        image=logo_image,
        compound="left",
        font=("Arial Black", 28),
        text_color="black"
    )
    title_label.pack(side="left", padx=40, pady=20)

    btn_exit = customtkinter.CTkButton(
        header,
        text="Sair",
        width=120,
        height=35,
        corner_radius=15,
        font=("Arial", 14, "bold"),
        fg_color="#000000",
        hover_color="#cfe2ff",
        text_color="white",
        command=lambda: window.destroy()
    )
    btn_exit.pack(side="right", padx=40)

    body = customtkinter.CTkFrame(main_frame, fg_color="#000000")
    body.pack(fill="both", expand=True, pady=(10, 0))

    content_frame = customtkinter.CTkFrame(body, fg_color="#394440", corner_radius=16)
    content_frame.pack(fill="both", expand=True, padx=30, pady=30)

    title_label = customtkinter.CTkLabel(
        content_frame,
        text="🧑‍🏫 Área do Professor",
        font=("Arial Black", 26),
        text_color="#000000"
    )
    title_label.pack(side="top", padx=40, pady=20)

    welcome_label = customtkinter.CTkLabel(
        content_frame,
        text=f"Bem-vindo, {user.get('name', 'Professor')}!",
        font=("Arial Black", 30),
        text_color="#000000"
    )
    welcome_label.pack(pady=(40, 20))

    info_label = customtkinter.CTkLabel(
        content_frame,
        text="Acesse suas turmas abaixo:",
        font=("Arial", 18),
        text_color="#FFFFFF"
    )
    info_label.pack(pady=(0, 40))

    btn_classes = customtkinter.CTkButton(
        content_frame,
        text="Minhas Turmas",
        width=250,
        height=60,
        corner_radius=15,
        font=("Arial Black", 20),
        fg_color="#000000",
        hover_color="#91afdb",
        command=lambda: classes_window(window)
    )
    btn_classes.pack()

    fade_in(window)
    window.mainloop()

if __name__ == "__main__":
    teacher_window({'name': 'Professor'})
