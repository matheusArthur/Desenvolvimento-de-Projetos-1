import os
import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, url_for

BASE = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["DATABASE"] = BASE / "tarefas.sqlite3"


def banco():
    if "banco" not in g:
        g.banco = sqlite3.connect(app.config["DATABASE"])
        g.banco.row_factory = sqlite3.Row
        g.banco.execute("PRAGMA foreign_keys = ON")
    return g.banco


@app.teardown_appcontext
def fechar_banco(_erro):
    conexao = g.pop("banco", None)
    if conexao is not None:
        conexao.close()


def iniciar_banco():
    banco().executescript((BASE / "schema.sql").read_text(encoding="utf-8"))


@app.get("/")
def inicio():
    tarefas = banco().execute(
        """SELECT tarefa.*, disciplina.nome AS disciplina
           FROM tarefa JOIN disciplina ON disciplina.id = tarefa.disciplina_id
           ORDER BY tarefa.prazo, tarefa.id"""
    ).fetchall()
    return render_template("lista.html", tarefas=tarefas)


@app.route("/disciplinas/nova", methods=["GET", "POST"])
def nova_disciplina():
    nome = request.form.get("nome", "").strip()
    erro = None
    if request.method == "POST":
        if 1 <= len(nome) <= 80:
            with banco() as conexao:
                conexao.execute("INSERT INTO disciplina (nome) VALUES (?)", (nome,))
            return redirect(url_for("nova_tarefa"), code=303)
        erro = "Informe um nome de até 80 caracteres."
    return render_template("disciplina.html", nome=nome, erro=erro)


def buscar_tarefa(tarefa_id):
    tarefa = banco().execute("SELECT * FROM tarefa WHERE id = ?", (tarefa_id,)).fetchone()
    if tarefa is None:
        abort(404)
    return dict(tarefa)


def exibir_formulario(tarefa=None):
    disciplinas = banco().execute("SELECT * FROM disciplina ORDER BY nome, id").fetchall()
    editando = tarefa is not None
    dados = tarefa or {"titulo": "", "prazo": "", "disciplina_id": "", "status": "Pendente"}
    erro = None

    if request.method == "POST":
        dados = {
            "titulo": request.form.get("titulo", "").strip(),
            "prazo": request.form.get("prazo", ""),
            "disciplina_id": request.form.get("disciplina_id", ""),
            "status": request.form.get("status", "") if editando else "Pendente",
        }
        try:
            prazo = date.fromisoformat(dados["prazo"]).isoformat()
        except ValueError:
            prazo = None
        disciplina = next((d for d in disciplinas if str(d["id"]) == dados["disciplina_id"]), None)

        if not 1 <= len(dados["titulo"]) <= 120:
            erro = "Informe um título de até 120 caracteres."
        elif prazo is None:
            erro = "Informe uma data válida."
        elif disciplina is None:
            erro = "Selecione uma disciplina cadastrada."
        elif dados["status"] not in ("Pendente", "Concluída"):
            erro = "Selecione uma situação válida."
        else:
            valores = (dados["titulo"], prazo, disciplina["id"], dados["status"])
            with banco() as conexao:
                if editando:
                    resultado = conexao.execute(
                        "UPDATE tarefa SET titulo = ?, prazo = ?, disciplina_id = ?, status = ? WHERE id = ?",
                        (*valores, tarefa["id"]),
                    )
                    if resultado.rowcount == 0:
                        abort(404)
                else:
                    conexao.execute(
                        "INSERT INTO tarefa (titulo, prazo, disciplina_id, status) VALUES (?, ?, ?, ?)",
                        valores,
                    )
            return redirect(url_for("inicio"), code=303)

    return render_template(
        "tarefa.html", dados=dados, disciplinas=disciplinas, editando=editando, erro=erro
    )


@app.route("/tarefas/nova", methods=["GET", "POST"])
def nova_tarefa():
    return exibir_formulario()


@app.route("/tarefas/<int:tarefa_id>/editar", methods=["GET", "POST"])
def editar_tarefa(tarefa_id):
    return exibir_formulario(buscar_tarefa(tarefa_id))


@app.route("/tarefas/<int:tarefa_id>/excluir", methods=["GET", "POST"])
def excluir_tarefa(tarefa_id):
    tarefa = buscar_tarefa(tarefa_id)
    if request.method == "POST":
        with banco() as conexao:
            resultado = conexao.execute("DELETE FROM tarefa WHERE id = ?", (tarefa_id,))
            if resultado.rowcount == 0:
                abort(404)
        return redirect(url_for("inicio"), code=303)
    return render_template("excluir.html", tarefa=tarefa)


@app.errorhandler(404)
def informar_pagina_ausente(_erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        iniciar_banco()
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
