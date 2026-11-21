# Tarefas acadêmicas

Desenvolvimento de Projetos I. O sistema organiza tarefas por disciplina e permite cadastrar, consultar, editar e excluir tarefas. Trabalho individual de Matheus Arthur Ferreira Silva (@matheusArthur).

## Como executar no Windows

No Windows, abra Iniciar.bat com dois cliques. Na primeira vez, o arquivo instala o Flask. Deixe a janela aberta e acesse http://127.0.0.1:5000 no navegador.

Para executar passo a passo, abra o PowerShell na pasta que contém `app.py` e rode os comandos abaixo, um de cada vez. É necessário ter Python 3.10 ou superior.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Abra http://127.0.0.1:5000 no navegador. Use Ctrl+C no PowerShell para encerrar.
Se `py` não estiver disponível, use `python` no primeiro comando.
Se a porta estiver ocupada, execute `$env:PORT = '5001'` antes de iniciar e abra http://127.0.0.1:5001.

## Como demonstrar

1. Cadastre a disciplina Banco de Dados.
2. Cadastre a tarefa Revisar DER e selecione a disciplina e um prazo.
3. Confira o título, a disciplina, o prazo e a situação na lista.
4. Encerre e inicie o servidor para verificar que a tarefa continua salva.
5. Edite a tarefa e marque como Concluída.
6. Abra a tela de exclusão. Cancele uma vez e confirme em seguida.
7. Abra **Disciplinas**, selecione **Excluir** e confirme. Se houver tarefas vinculadas, mova ou exclua essas tarefas primeiro.

## Estrutura

- `app.py` recebe as ações do navegador, valida os formulários e executa os comandos SQL.
- `schema.sql` define as tabelas e o relacionamento.
- `templates/` contém as páginas HTML. `static/` contém o CSS.
- `tarefas.sqlite3` é criado na primeira execução. O arquivo fica no computador e é ignorado pelo Git.
