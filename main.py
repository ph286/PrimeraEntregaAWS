from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

@app.get("/")
def read_root():
    dns = "http://ec2-34-230-77-19.compute-1.amazonaws.com"
    return {
        "_links": {
            "students": {
                "href": f"{dns}/alumnos{{?page,size,sort*}}",
                "templated": True
            },
            "teachers": {
                "href": f"{dns}/profesores{{?page,size,sort*}}",
                "templated": True
            },
            "profile": {
                "href": f"{dns}/profile"
            }
        }
    }

# --- SOLUCIÓN PARA EL AUTOTEST: Convertir 422 en 400 ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()}
    )

# --- MODELOS ---
class Alumno(BaseModel):
    id: int
    nombres: str = Field(..., min_length=1) # No permite vacíos
    apellidos: str = Field(..., min_length=1)
    matricula: str = Field(..., min_length=1)
    promedio: float

class Profesor(BaseModel):
    id: int
    numeroEmpleado: int
    nombres: str = Field(..., min_length=1)
    apellidos: str = Field(..., min_length=1)
    horasClase: int

# Base de datos en memoria 
db_alumnos = []
db_profesores = []

# --- ENDPOINTS ALUMNOS ---
@app.get("/alumnos", response_model=List[Alumno])
async def get_alumnos():
    return db_alumnos

@app.post("/alumnos", status_code=201)
async def create_alumno(alumno: Alumno):
    db_alumnos.append(alumno)
    return alumno

@app.get("/alumnos/{id}")
async def get_alumno(id: int):
    for a in db_alumnos:
        if a.id == id:
            return a
    raise HTTPException(status_code=404, detail="No encontrado")

@app.put("/alumnos/{id}")
async def update_alumno(id: int, upd: Alumno):
    for i, a in enumerate(db_alumnos):
        if a.id == id:
            db_alumnos[i] = upd
            return upd
    raise HTTPException(status_code=404, detail="No encontrado")

@app.delete("/alumnos/{id}")
async def delete_alumno(id: int):
    for i, a in enumerate(db_alumnos):
        if a.id == id:
            del db_alumnos[i]
            return {"msg": "Eliminado"}
    raise HTTPException(status_code=404, detail="No encontrado")

# --- ENDPOINTS PROFESORES ---
@app.get("/profesores", response_model=List[Profesor])
async def get_profesores():
    return db_profesores

@app.post("/profesores", status_code=201)
async def create_profesor(prof: Profesor):
    db_profesores.append(prof)
    return prof

@app.get("/profesores/{id}")
async def get_profesor(id: int):
    for p in db_profesores:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="No encontrado")

@app.put("/profesores/{id}")
async def update_profesor(id: int, upd: Profesor):
    for i, p in enumerate(db_profesores):
        if p.id == id:
            db_profesores[i] = upd
            return upd
    raise HTTPException(status_code=404, detail="No encontrado")

@app.delete("/profesores/{id}")
async def delete_profesor(id: int):
    for i, p in enumerate(db_profesores):
        if p.id == id:
            del db_profesores[i]
            return {"msg": "Eliminado"}
    raise HTTPException(status_code=404, detail="No encontrado")
