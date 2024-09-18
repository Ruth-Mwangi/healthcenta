from typing import List
from pydantic import BaseModel


class ServiceProvider(BaseModel):
    id: int
    price: float

class Department(BaseModel):
    name: str

class Specialty(BaseModel):
    name: str

class Category(BaseModel):
    name: str

class NatureOfProcedure(BaseModel):
    name: str

class ServiceData(BaseModel):
    name: str
    product_index: str
    department: Department
    speciality: Specialty
    category: Category
    nature_of_procedure: NatureOfProcedure
    service_providers: List[ServiceProvider]