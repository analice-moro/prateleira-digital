from models.item_catalogo.itemCatalogo import ItemCatalogo
from models.item_catalogo.avaliacoes import Avaliacoes

class Disco(ItemCatalogo):
    def __init__(self, titulo, artista, ano_lancamento, genero, formato_midia, preco):
        super().__init__(titulo, genero,  ano_lancamento, preco)
        self._artista = artista
        self._formato_midia = formato_midia
        self._avaliacoes = []

    def avaliar_disco(self, cliente, nota):
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
