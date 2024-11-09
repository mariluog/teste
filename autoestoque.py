# MEU PRIMEIRO WEB APP
import streamlit as st
from ACTlib01 import *

#url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQFwxxM13bxUC0dpyd0w0PxfZIrJ-hp4Px-R6rsTiG3c3n-89JApzA0jYJpU9vNfxeNCvtJ0Cg35KtO/pub?gid=556192647&single=true&output=csv"
#db = Ler_GooglePlanilha(url)
#db.fillna('', inplace=True)
#Escrever(db)

# Use st.title("") para adicionar um TÍTULO ao seu Web app
st.title("MEU 1º WEB APP STREAMLIT")

# Use st.header("") para adicionar um CABEÇALHO ao seu Web app
st.header("Hejheheheh! Prof. Massaki")

# Use st.subheader("") para adicionar um SUB CABEÇALHO ao seu Web app
st.subheader("Sub Cabeçalho")

# Use st.write("") para adicionar um texto ao seu Web app
st.write("Como já deve ter percebido, o método st.write() é usado para escrita de texto e informações gerais!")

values = st.slider("Select a range of values", 0.0, 100.0, (5.0, 15.0))
st.write("Values:", values)

st.image("desenvolvimento.jpg", caption="TESTE_Inserir_IMAGEM")




import json
import os

class Item:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.nome} - Quantidade: {self.quantidade}, Preço: R${self.preco:.2f}"

    # Método para facilitar a serialização do objeto Item em JSON
    def to_dict(self):
        return {"nome": self.nome, "quantidade": self.quantidade, "preco": self.preco}

    # Método para criar um objeto Item a partir de um dicionário
    @staticmethod
    def from_dict(data):
        return Item(data["nome"], data["quantidade"], data["preco"])

class Estoque:
    def __init__(self, arquivo_estoque="estoque.json"):
        self.itens = {}
        self.arquivo_estoque = arquivo_estoque
        self.carregar_estoque()

    def adicionar_item(self, nome, quantidade, preco):
        if nome in self.itens:
            self.itens[nome].quantidade += quantidade
        else:
            self.itens[nome] = Item(nome, quantidade, preco)

    def remover_item(self, nome, quantidade):
        if nome in self.itens:
            if self.itens[nome].quantidade >= quantidade:
                self.itens[nome].quantidade -= quantidade
                if self.itens[nome].quantidade == 0:
                    del self.itens[nome]
            else:
                print("Quantidade insuficiente para remover.")
        else:
            print("Item não encontrado.")

    def listar_itens(self):
        if not self.itens:
            print("Estoque vazio.")
        else:
            for item in self.itens.values():
                print(item)

    def valor_total_estoque(self):
        total = sum(item.quantidade * item.preco for item in self.itens.values())
        return total

    def salvar_estoque(self):
        # Salva o estoque no arquivo JSON
        with open(self.arquivo_estoque, "w") as f:
            json.dump({nome: item.to_dict() for nome, item in self.itens.items()}, f, indent=4)

    def carregar_estoque(self):
        # Carrega o estoque do arquivo JSON, se existir
        if os.path.exists(self.arquivo_estoque):
            with open(self.arquivo_estoque, "r") as f:
                dados = json.load(f)
                for nome, item_data in dados.items():
                    self.itens[nome] = Item.from_dict(item_data)

def menu():
    estoque = Estoque()  # Carrega o estoque do arquivo automaticamente
    while True:
        print("\n--- Sistema de Organização de Estoque ---")
        print("1. Adicionar Item")
        print("2. Remover Item")
        print("3. Listar Itens")
        print("4. Valor Total do Estoque")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do item: ")
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
            estoque.adicionar_item(nome, quantidade, preco)
            print(f"Item '{nome}' adicionado com sucesso!")

        elif opcao == '2':
            nome = input("Nome do item: ")
            quantidade = int(input("Quantidade a remover: "))
            estoque.remover_item(nome, quantidade)

        elif opcao == '3':
            print("\nItens no Estoque:")
            estoque.listar_itens()

        elif opcao == '4':
            total = estoque.valor_total_estoque()
            print(f"\nValor total do estoque: R${total:.2f}")

        elif opcao == '5':
            # Antes de sair, salva o estoque no arquivo
            estoque.salvar_estoque()
            print("Saindo do sistema...")

            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
     
