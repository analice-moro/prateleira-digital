# Prateleira Digital

Site de vendas de **livros, revistas e discos** com visual aconchegante, inspirado em livrarias e sebos. Lojas parceiras se cadastram, passam por aprovação de um administrador e montam o próprio catálogo. Os usuários navegam pelas lojas, veem os produtos e deixam avaliações.
 
> Projeto desenvolvido em Flask com MySQL, usando HTML e CSS puros no front-end.

---

## Funcionalidades

- Cadastro e login de usuários, com senha armazenada em hash.
- Página inicial pública com as lojas aprovadas, mostrando nome, cidade e média de avaliações.
- Painel com os produtos de todas as lojas ativas, separados em abas: livros, revistas e discos.
- Cadastro de lojas, que ficam pendentes até a aprovação de um administrador.
- Bloqueio de lojas repetidas (mesmo nome na mesma cidade, sem diferenciar maiúsculas).
- Catálogo por loja, com cadastro de produtos e upload da capa.
- Avaliação de lojas e de produtos, com notas de 1 a 5 estrelas.
- Área de administração para aprovar lojas, alterar o status e remover lojas e produtos.

---

## Navegação

**1. Visitante (sem login)**
A página inicial (`/`) lista as lojas com status **Ativo**, em cards com nome, cidade e média de avaliações. Se não houver nenhuma, aparece a mensagem *"Ainda não temos lojas ativas por aqui. Volte em breve!"*. O cabeçalho oferece os links **Cadastro** e **Login**. Todas as demais telas exigem login.
 
**2. Painel (`/painel`)**
Depois de entrar, o usuário chega ao painel, que reúne os produtos das lojas ativas em três abas (Livros, Revistas e Discos), cada uma com contador. Clicar em um card abre o detalhe do produto. No cabeçalho ficam os botões **Ver lojas** e **Sair**; administradores veem também o link **Administração**.
 
**3. Lojas (`/lojas`)**
Lista apenas as lojas ativas, em cards com nome, cidade e média de avaliações. No cabeçalho há o botão **Cadastrar loja**. Uma loja nova entra como **Pendente** e só aparece no site depois de aprovada.
 
**4. Detalhe da loja (`/loja/<id>`)**
Mostra as informações da loja, a média, todas as avaliações recebidas e três ações: **Ver produtos**, **Adicionar produto** e **Avaliar**.
 
**5. Catálogo da loja (`/loja/<id>/catalogo`)**
Exibe os produtos da loja em abas por tipo. Cada card leva ao detalhe do produto. Administradores veem também o botão **Remover produto**.
 
**6. Detalhe do produto (`/item/<id>`)**
Mostra capa, tipo, título, autor/editora/artista, gênero, ano, preço, média e avaliações. Os botões são **Avaliar** e **Ver loja**, que leva à loja que vende o produto.
 
**7. Administração (apenas administradores)**
- `/admin`: lojas pendentes, com o botão **Aprovar loja**.
- `/admin/lojas`: todas as lojas, com seletor para alterar o status e botão para remover a loja.
Remover uma loja apaga também os produtos e as avaliações dela.

## Ferramentas utilizadas

| Camada | Ferramenta | Uso no projeto |
|---|---|---|
| Linguagem | **Python 3** | Back-end e regras de negócio |
| Framework web | **Flask** | Rotas, sessões, mensagens flash e upload de arquivos |
| Templates | **Jinja2** | Páginas HTML dinâmicas |
| Segurança | **Werkzeug** | Hash de senha e nome seguro de arquivos |
| Banco de dados | **MySQL** | Armazenamento de usuários, lojas, produtos e avaliações |
| Conexão | **mysql-connector-python** | Acesso ao MySQL |
| Configuração | **python-dotenv** | Variáveis de ambiente (`.env`) |
| Front-end | **HTML5, CSS3 e JavaScript** | Interface responsiva, sem frameworks de CSS |
| Fontes | **Google Fonts** | Playfair Display (títulos) e Lora (texto) |
 
**Organização do código:** o projeto usa orientação a objetos nos modelos (`Usuario`, `Loja`, `Livro`, `Revista`, `Disco`, `Avaliacoes`) e o padrão de repositórios, em que cada arquivo de `repositories/` concentra as consultas SQL de uma entidade.
 
---
 
## Identidade visual
 
| Elemento | Valor |
|---|---|
| Fundo | `#FDFBF7` |
| Texto | `#382621` |
| Cabeçalho | `#8B2628` |
| Botões, ícones e detalhes | `#C85A32` |
| Títulos | Playfair Display (serifada) |
| Texto corrido | Lora (serifada) |
 
Botões e cards usam sombras suaves e cantos arredondados, e o layout se adapta a telas de celular.