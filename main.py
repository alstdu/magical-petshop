from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Create the FastAPI application
app = FastAPI(title="Magical Pet Shop API")

# This will be our data model for a pet
class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    species: str
    magical_ability: str
    age: int

# This will be our "database" (just a list for now)
magical_pets = [
    Pet(id=1, name="Sparkles", species="Dragon", magical_ability="Breathes rainbow fire", age=3),
    Pet(id=2, name="Luna", species="Unicorn", magical_ability="Grants wishes", age=5),
    Pet(id=3, name="Shadow", species="Phoenix", magical_ability="Resurrects from ashes", age=1000)
]

# Get all pets
@app.get("/pets", response_model=List[Pet])
async def get_all_pets():
    return magical_pets

# Get a specific pet by ID
@app.get("/pets/{pet_id}")
async def get_pet(pet_id: int):
    for pet in magical_pets:
        if pet.id == pet_id:
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")

## TODO: investigate id collision bug if pets are adopted
# Add a new pet
@app.post("/pets", response_model=Pet)
async def create_pet(pet: Pet):
    pet.id = len(magical_pets) + 1
    magical_pets.append(pet)
    return pet

# Adopt (delete) a pet
@app.delete("/pets/{pet_id}")
async def adopt_pet(pet_id: int):
    for i, pet in enumerate(magical_pets):
        if pet.id == pet_id:
            return magical_pets.pop(i)
    raise HTTPException(status_code=404, detail="Pet not found") 
