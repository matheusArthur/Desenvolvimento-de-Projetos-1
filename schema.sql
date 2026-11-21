CREATE TABLE IF NOT EXISTS disciplina (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL CHECK (length(trim(nome)) BETWEEN 1 AND 80)
);

CREATE TABLE IF NOT EXISTS tarefa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL CHECK (length(trim(titulo)) BETWEEN 1 AND 120),
    prazo TEXT NOT NULL,
    disciplina_id INTEGER NOT NULL REFERENCES disciplina(id),
    status TEXT NOT NULL DEFAULT 'Pendente' CHECK (status IN ('Pendente', 'Concluída'))
);
