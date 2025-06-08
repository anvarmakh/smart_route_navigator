# Управление сотрудниками компании: добавление водителей и просмотр списка
from fastapi import APIRouter
from app.services.company_service import get_drivers, add_driver

router = APIRouter()

@router.get("/drivers")
def list_drivers(company_id: int):
    """Получение списка водителей, привязанных к компании"""
    return get_drivers(company_id)

@router.post("/drivers")
def create_driver(company_id: int, driver_data: dict):
    """Добавление нового водителя в компанию по company_id"""
    return add_driver(company_id, driver_data)
