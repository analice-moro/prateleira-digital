from models.item_catalogo.itemCatalogo import ItemCatalogo
from models.item_catalogo.avaliacoes import Avaliacoes

class Livro(ItemCatalogo):
    def __init__(self, titulo, autor, ano_lancamento, genero, preco, sinopse):
        super().__init__(titulo, genero, ano_lancamento, preco)
        self._autor = autor
        self._sinopse = sinopse
        self._avaliacoes = []

    def avaliar_livro(self, cliente, nota):
        avaliacao = Avaliacoes(cliente, nota)
        self._avaliacoes.append(avaliacao)

    @property
    def media_avaliacoes(self):
        if not self._avaliacoes:
            return 0.0
        notas_somadas = sum(avaliacao._nota for avaliacao in self._avaliacoes)
        quantidade_avaliacoes = len(self._avaliacoes)
        media = round(notas_somadas / quantidade_avaliacoes, 1)
        return media
