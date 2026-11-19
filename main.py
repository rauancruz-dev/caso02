from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API REST - Cadastro de Alunos")

class AlunoCreate(BaseModel):
    nome: str
    matricula: str
    curso: str

class Aluno(AlunoCreate):
    id: int

banco_alunos: List[Aluno] = []
contador_id = 1

@app.post("/alunos", response_model=Aluno, status_code=201)
def cadastrar_aluno(dados: AlunoCreate):
    global contador_id
    novo_aluno = Aluno(id=contador_id, **dados.model_dump())
    banco_alunos.append(novo_aluno)
    contador_id += 1
    return novo_aluno

@app.get("/alunos", response_model=List[Aluno])
def listar_alunos():
    return banco_alunos

@app.get("/alunos/{id}", response_model=Aluno)
def consultar_aluno(id: int):
    for aluno in banco_alunos:
        if aluno.id == id:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")