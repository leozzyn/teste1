import customtkinter
from os import path
from PIL import Image
from tkcalendar import Calendar
from db_load import load_database, save_database

def get_user_by_name(name):
    try:
        data = load_database()
        users = data.get("users", [])
        for user in users:
            if user["name"] == name:
                return user
    except Exception as e:
        customtkinter.messagebox.showerror("Erro", f"Falha ao acessar o servidor:\n{e}")
    return None

def fade_in(window, step=0.05, delay=10):
    if not window.winfo_exists():
        return
    window.attributes("-alpha", 0)
    window.update()
    for i in range(0, 21):
        if not window.winfo_exists():
            return
        window.attributes("-alpha", i * step)
        window.update()
        window.after(delay)

def fade_out(window, step=0.05, delay=10):
    if not window.winfo_exists():
        return
    for i in reversed(range(0, 21)):
        if not window.winfo_exists():
            return
        window.attributes("-alpha", i * step)
        window.update()
        window.after(delay)

def destroy_previous(previous_window):
    if previous_window and previous_window.winfo_exists():
        fade_out(previous_window)
        previous_window.destroy()

def student_area_window(user, previous_window):
    destroy_previous(previous_window)
    new_window = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}+0+0")
    new_window.attributes("-fullscreen", True)
    new_window.title(f"Minhas Informações - {user['name']}")

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
        font=("Arial Black", 28),
        text_color="black",
        command=lambda: student_window(user, new_window)
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

    content_frame = customtkinter.CTkFrame(main_frame, fg_color="#394440", corner_radius=16)
    content_frame.pack(fill="both", expand=True, padx=40, pady=30)

    grades = user.get("school_grades", {})

    if grades:
        title_grades = customtkinter.CTkLabel(
            content_frame,
            text="👤 Suas Notas",
            font=("Arial Black", 22),
            text_color="#000000"
        )
        title_grades.pack(pady=(20, 10))

        for n_key, n_value in grades.items():
            grade_label = customtkinter.CTkLabel(
                content_frame,
                text=f"{n_key}: {n_value:.1f}",
                font=("Arial", 20),
                text_color="#FFFFFF"
            )
            grade_label.pack(pady=5)

        average = sum(grades.values()) / len(grades)
        average_frame = customtkinter.CTkFrame(
            content_frame,
            fg_color="#e6f2ff",
            corner_radius=20,
            border_width=2,
            border_color="#004aad"
        )
        average_frame.pack(pady=30, ipadx=30, ipady=20)

        average_label_title = customtkinter.CTkLabel(
            average_frame,
            text="Média Final",
            font=("Arial Black", 22),
            text_color="#3a3b3b"
        )
        average_label_title.pack(pady=(5, 0))

        average_label = customtkinter.CTkLabel(
            average_frame,
            text=f"{average:.2f}",
            font=("Arial Black", 36),
            text_color="#007acc"
        )
        average_label.pack(pady=(0, 10))

        if average >= 7:
            status = "🟢 Aprovado"
            color_status = "#2ecc71"
        elif average >= 5:
            status = "🟡 Recuperação"
            color_status = "#f1c40f"
        else:
            status = "🔴 Reprovado"
            color_status = "#e74c3c"

        average_status = customtkinter.CTkLabel(
            average_frame,
            text=status,
            font=("Arial", 16, "bold"),
            text_color=color_status
        )
        average_status.pack(pady=(0, 10))

    else:
        info_label = customtkinter.CTkLabel(
            content_frame,
            text="Nenhuma nota disponível.",
            font=("Arial", 18),
            text_color="#000000"
        )
        info_label.pack(pady=60)

    fade_in(new_window)

def calendar_window(user, previous_window):
    destroy_previous(previous_window)
    new_window = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}+0+0")
    new_window.attributes("-fullscreen", True)
    new_window.title("Calendário Acadêmico")

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
        command=lambda: student_window(user, new_window)
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

    content_frame = customtkinter.CTkFrame(main_frame, fg_color="#394440", corner_radius=16)
    content_frame.pack(fill="both", expand=True, padx=40, pady=30)

    title_label = customtkinter.CTkLabel(
        content_frame,
        text="📅 Calendário Acadêmico",
        font=("Arial Black", 26),
        text_color="#000000"
    )
    title_label.pack(side="top", padx=40, pady=20)

    cal = Calendar(
        content_frame,
        selectmode="day",
        year=2025,
        month=10,
        day=18,
        locale="pt_BR",
        date_pattern="dd/mm/yyyy",
        background="white",
        foreground="black",
        selectbackground="#005f99",
        selectforeground="white",
        bordercolor="#005f99"
    )
    cal.pack(pady=20)

    selected_date_label = customtkinter.CTkLabel(content_frame, text="", font=("Arial", 14))
    selected_date_label.pack(pady=10)

    def show_date():
        data = cal.get_date()
        selected_date_label.configure(text=f"Data selecionada: {data}")

    btn_show = customtkinter.CTkButton(
        content_frame,
        text="Ver Data Selecionada",
        command=show_date,
        width=180,
        height=35,
        fg_color="#005f99",
        hover_color="#cfe2ff",
        text_color="white"
    )
    btn_show.pack(pady=(0, 20))

    fade_in(new_window)

def student_window(user, previous_window=None):
    destroy_previous(previous_window)
    new_window = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("blue")
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}+0+0")
    new_window.attributes("-fullscreen", True)
    new_window.title("Início")
    new_window.attributes("-alpha", 0)

    main_frame = customtkinter.CTkFrame(new_window, fg_color="#000000")
    main_frame.pack(fill="both", expand=True)

    header = customtkinter.CTkFrame(main_frame, fg_color="#6d7675", height=80, corner_radius=0)
    header.pack(fill="x", side="top")

    logo_image = customtkinter.CTkImage(dark_image=Image.open("assets/img/logo.png"), size=(40, 70))
    title_label = customtkinter.CTkLabel(
        header,
        text="  BRISPACE",
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
        command=lambda: fade_out(new_window) or new_window.destroy()
    )
    btn_exit.pack(side="right", padx=40)

    content_frame = customtkinter.CTkFrame(main_frame, fg_color="#394440", corner_radius=16)
    content_frame.pack(fill="both", expand=True, padx=40, pady=30)

    subtitle = customtkinter.CTkLabel(
        content_frame,
        text=f"Por onde começar, {user['name']}?",
        font=("Arial Black", 18),
        text_color="black"
    )
    subtitle.pack(pady=(40, 20))

    icon_path = "assets/student_window"
    def load_icon(filename, size=(40, 40)):
        img_path = path.join(icon_path, filename)
        return customtkinter.CTkImage(
            dark_image=Image.open(img_path),
            light_image=Image.open(img_path),
            size=size
        )

    buttons = [
        ("Área do Aluno", "aluno.png", student_area_window),
        ("Calendário", "calendario.png", calendar_window),
    ]

    btn_frame = customtkinter.CTkFrame(content_frame, fg_color="#394440")
    btn_frame.pack(pady=80)

    for idx, (text, icon_name, command) in enumerate(buttons):
        icon = load_icon(icon_name)
        btn = customtkinter.CTkButton(
            btn_frame,
            text=f"  {text}  ",
            image=icon,
            compound="left",
            anchor="w",
            width=300,
            height=80,
            corner_radius=15,
            font=("Arial", 18, "bold"),
            fg_color="#6d7675",
            text_color="black",
            border_color="#000000",
            border_width=2,
            hover_color="#cfe2ff",
            command=lambda cmd=command: cmd(user, new_window)
        )
        btn.grid(row=0, column=idx, padx=30, pady=20, sticky="nsew")

    fade_in(new_window)
    new_window.bind("<Escape>", lambda event: new_window.attributes("-fullscreen", False))
    new_window.mainloop()


if __name__ == "__main__":
    student_window({'name': 'Nome do Aluno'}, previous_window=None)
