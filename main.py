from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import tabela_loja, tabela_avaliacao
from models.loja import Loja
from models.item_catalogo.livro import Livro
from models.item_catalogo.discos import Disco
from models.item_catalogo.revista import Revista
from models.item_catalogo.avaliacoes import Avaliacoes
from repositories import loja_repo
from repositories import usuario_repo
from repositories import avaliacoes_repo
from repositories import catalogo_repo

app = Flask(__name__)
app.secret_key = "3itaQue-ch4veDlfic1l"

