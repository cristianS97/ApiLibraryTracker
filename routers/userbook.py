from fastapi import APIRouter

router = APIRouter(prefix="/userbook", tags=["Gestión de mi librería"])

router.get("/")
def obtener_mi_libreria():
    return { 'librería': 'ok' }