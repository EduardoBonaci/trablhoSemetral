import tkinter as tk 

janela = tk.Tk()
janela.title("sistema de biblioteca")


#criando rotulo 
lbl_user = tk.Label(text="usuario")
lbl_user.pack()

txt_user = tk.Entry()
txt_user.pack()


lbl_senha = tk.Label(text="senha")
lbl_senha.pack()

txt_senha = tk.Entry()
txt_senha.pack()


button  = tk.Button()
button.pack()

janela.mainloop()