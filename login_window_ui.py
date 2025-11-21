import customtkinter
from os import path
from db_load import load_database
from pyautogui import alert
from PIL import Image
from student_window_ui import student_window
from teacher_window_ui import teacher_window

def login_window():
    window = customtkinter.CTk(fg_color="#394440")
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}+0+0")
    window.attributes("-fullscreen", True)
    window.title("Login")

    window.columnconfigure(0, weight=1)
    for r in range(10):
        window.rowconfigure(r, weight=1)

    logo_path = "assets/img/output_logo.png"
    if path.exists(logo_path):
        logo_image = customtkinter.CTkImage(
            light_image=Image.open(logo_path), 
            dark_image=Image.open(logo_path), 
            size=(190, 170)
        )
        logo_label = customtkinter.CTkLabel(window, image=logo_image, text="")
        logo_label.grid(row=0, column=0, pady=(40, 10), sticky="n")
    else:
        logo_label = customtkinter.CTkLabel(window, text="BRISPACE", font=("Arial Black", 28))
        logo_label.grid(row=0, column=0, pady=(40, 10), sticky="n")

    entry_email = customtkinter.CTkEntry(window, placeholder_text="E-mail", width=300, height=40)
    entry_email.grid(row=1, column=0, pady=8)
    entry_password = customtkinter.CTkEntry(window, placeholder_text="Senha", show="*", width=300, height=40)
    entry_password.grid(row=2, column=0, pady=8)

    login_button = customtkinter.CTkButton(
        window, text="Entrar", 
        command=lambda: getDataClient(),
        width=100, height=40,
        font=("Arial", 14, "bold"),
        fg_color="#000000", hover_color="#005f99"
    )
    login_button.grid(row=3, column=0, pady=(20, 10))

    def getDataClient():
        email = entry_email.get()
        password = entry_password.get()

        try:
            data = load_database()
            users = data.get("users", [])
        except Exception as e:
            alert(text=f"Falha ao acessar o servidor:\n{e}", title="ERRO", button="OK")
            return

        for user in users:
            if user.get("email") == email and user.get("password") == password:
                print(f"✅ Login efetuado com sucesso\n✅ Token de Acesso: {user.get('token')}")
                alert(text=f'Bem‑vindo, {user.get("name")}!', title='✅ LOGIN', button='OK')

                if user.get("token") == 1:
                    window.destroy()
                    teacher_window(user)
                elif user.get("token") == 2:
                    window.destroy()
                    student_window(user)
                return

        print("❌ Falha no Login")
        alert(text='Verifique as informações de login e tente novamente.', title='ERRO', button='OK')

    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))
    window.mainloop()

if __name__ == "__main__":
    login_window()
