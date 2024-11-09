import streamlit as st
import json
import os

class Item:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.nome} - Quantidade: {self.quantidade}, Preço: R${self.preco:.2f}"

    def to_dict(self):
        return {"nome": self.nome, "quantidade": self.quantidade, "preco": self.preco}

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
                self.itens[nome].quantidade 
