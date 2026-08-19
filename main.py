from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
from models import ProdutoDB, PetDB  
from schemas import ProdutoCreate, ProdutoResponse, PetCreate, PetResponse 

Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'], 
        allow_methods=['*'],
        allow_headers=['*'],
    )



@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()


@app.post("/produtos", response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
        
    return produto

@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
        
    db.delete(produto)
    db.commit()

@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
        
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    
    db.commit()
    db.refresh(produto)
    return produto






@app.get("/pets", response_model=list[PetResponse])
def listar_pets(db: Session = Depends(get_db)):
    return db.query(PetDB).all()


@app.post("/pets", response_model=PetResponse, status_code=201)
def criar_pet(pet: PetCreate, db: Session = Depends(get_db)):
    novo_pet = PetDB(**pet.dict())
    db.add(novo_pet)
    db.commit()
    db.refresh(novo_pet)
    return novo_pet


@app.get('/pets/{pet_id}', response_model=PetResponse)
def obter_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetDB).filter(PetDB.id == pet_id).first()
    
    if pet is None:
        raise HTTPException(status_code=404, detail='Pet não encontrado')
        
    return pet


@app.put('/pets/{pet_id}', response_model=PetResponse)
def atualizar_pet(pet_id: int, pet_atualizado: PetCreate, db: Session = Depends(get_db)):
    pet = db.query(PetDB).filter(PetDB.id == pet_id).first()
    
    if pet is None:
        raise HTTPException(status_code=404, detail='Pet não encontrado')
    
    for chave, valor in pet_atualizado.dict().items():
        setattr(pet, chave, valor)
        
    db.commit()
    db.refresh(pet)
    return pet


@app.delete('/pets/{pet_id}', status_code=204)
def remover_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(PetDB).filter(PetDB.id == pet_id).first()
    
    if pet is None:
        raise HTTPException(status_code=404, detail='Pet não encontrado')
        
    db.delete(pet)
    db.commit()
