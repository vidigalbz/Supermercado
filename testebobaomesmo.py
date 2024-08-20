import tkinter as tk
from tkinter import messagebox

def adicionar_produto():
    produto = entrada_produto.get()
    if produto:
        lista_produtos.append(produto)
        atualizar_lista()
        entrada_produto.delete(0, tk.END)  # Limpa o campo de entrada
    else:
        messagebox.showwarning("Aviso", "O campo de produto está vazio.")

def atualizar_lista():
    texto_lista.delete(1.0, tk.END)  # Limpa o conteúdo atual da área de texto
    for produto in lista_produtos:
        texto_lista.insert(tk.END, f"{produto}\n")

# Cria a janela principal
root = tk.Tk()
root.title("Registro de Produtos")

# Lista para armazenar produtos
lista_produtos = []

# Cria widgets
rotulo = tk.Label(root, text="Nome do Produto:")
entrada_produto = tk.Entry(root)
botao_adicionar = tk.Button(root, text="Adicionar", command=adicionar_produto)
texto_lista = tk.Text(root, height=10, width=30)

# Organiza widgets na janela
rotulo.pack(pady=5)
entrada_produto.pack(pady=5)
botao_adicionar.pack(pady=5)
texto_lista.pack(pady=5)

# Inicia o loop principal do Tkinter
root.mainloop()
