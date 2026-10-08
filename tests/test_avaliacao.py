from models.item_catalogo.avaliacoes import Avaliacoes

def test_avaliacao_valida():
    avaliacao = Avaliacoes("Maria", 4.7)
    assert avaliacao._cliente == "Maria"
    assert avaliacao._nota == 4.7