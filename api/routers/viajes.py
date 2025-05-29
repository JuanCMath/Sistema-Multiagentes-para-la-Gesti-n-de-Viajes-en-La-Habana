from fastapi import APIRouter, HTTPException
from domain.schemas import  ViajeCreate, ViajeRead, ViajeUpdate
from domain.models import Viaje, Session
from typing import List

router = APIRouter()

@router.post("/viajes/", response_model=ViajeRead)
def crear_viaje(viaje: ViajeCreate):
    with Session() as session:
        nuevo_viaje = Viaje(**viaje.dict())
        session.add(nuevo_viaje)
        session.commit()
        session.refresh(nuevo_viaje)
        return nuevo_viaje

@router.get("/viajes/", response_model=List[ViajeRead])
def listar_viajes():
    with Session() as session:
        viajes = session.query(Viaje).all()
        return viajes

@router.get("/viajes/{viaje_id}", response_model=ViajeRead)
def obtener_viaje(viaje_id: int):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        return viaje

@router.delete("/viajes/{viaje_id}")
def eliminar_viaje(viaje_id: int):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        session.delete(viaje)
        session.commit()
        return {"status": "success", "message": "Viaje eliminado exitosamente."}


@router.put("/viajes/{viaje_id}", response_model=ViajeRead)
def actualizar_viaje(viaje_id: int, viaje_data: ViajeUpdate):
    with Session() as session:
        viaje = session.query(Viaje).filter_by(id=viaje_id).first()
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")

        for field, value in viaje_data.dict(exclude_unset=True).items():
            setattr(viaje, field, value)

        session.commit()
        session.refresh(viaje)
        return viaje
