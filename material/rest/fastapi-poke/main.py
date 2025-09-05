from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Pokemon(BaseModel):
    name: str
    type: str
    level: int
    hp: int
    attack: int
    defense: int
    speed: int
    description: str
    special: bool

@app.get("/ping")
def health_check():
    return {"ping": "pong"}

@app.get("/pokemons/")
def list_pokemons():
    return []

@app.get("/pokemons/{pokemon_id}")
def get_pokemon(pokemon_id: int):
    return {"pokemon_id": pokemon_id}

@app.post("/pokemons/")
def create_pokemon(pokemon: Pokemon):
    return {"pokemon": pokemon}

@app.put("/pokemons/{pokemon_id}")
def update_pokemon(pokemon_id: int, pokemon: Pokemon):
    return {"pokemon_id": pokemon_id, "pokemon": pokemon}

@app.delete("/pokemons/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    return {"pokemon_id": pokemon_id}

@app.head("/pokemons/{pokemon_id}")
def head_pokemon(pokemon_id: int):
    return {"pokemon_id": pokemon_id}