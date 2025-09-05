from datetime import date
from typing import List
from django.shortcuts import get_object_or_404

from ninja import NinjaAPI
from ninja import Schema

from .models import Aluno

class AlunoSchema(Schema):
    nome: str
    email: str
    data_nascimento: date 
    data_matricula: date 
    registro_academico: str

class AlunoSchemaOut(AlunoSchema):
    id: int

class AlunoSchemaOptional(AlunoSchema):
    nome: str = None
    email: str = None
    data_nascimento: date = None
    data_matricula: date = None
    registro_academico: str = None

# Create your views here.
api = NinjaAPI()

@api.get("/alunos", response=List[AlunoSchemaOut])
def listar_alunos(request):
    return Aluno.objects.all()

@api.get("/alunos/{aluno_id}", response=AlunoSchemaOut)
def buscar_aluno(request, aluno_id: int):
    return get_object_or_404(Aluno, id=aluno_id)

@api.post("/alunos", response=AlunoSchemaOut)
def criar_aluno(request, aluno: AlunoSchema):
    return Aluno.objects.create(**aluno.dict())

@api.put("/alunos/{aluno_id}", response=AlunoSchemaOut)
def atualizar_aluno(request, aluno_id: int, aluno: AlunoSchema):
    aluno_obj = get_object_or_404(Aluno, id=aluno_id)
    aluno_obj.nome = aluno.nome
    aluno_obj.email = aluno.email
    aluno_obj.data_nascimento = aluno.data_nascimento
    aluno_obj.data_matricula = aluno.data_matricula
    aluno_obj.registro_academico = aluno.registro_academico
    aluno_obj.save()
    return aluno_obj

@api.patch("/alunos/{aluno_id}", response=AlunoSchemaOut)
def atualizar_parcial_aluno(request, aluno_id: int, aluno: AlunoSchemaOptional):
    aluno_obj = get_object_or_404(Aluno, id=aluno_id)
    for attr, value in aluno.dict(exclude_unset=True).items():
        setattr(aluno_obj, attr, value)
    aluno_obj.save()
    return aluno_obj

@api.delete("/alunos/{aluno_id}")
def deletar_aluno(request, aluno_id: int):
    aluno_obj = get_object_or_404(Aluno, id=aluno_id)
    aluno_obj.delete()
    return {"message": "Aluno deletado com sucesso!"}


