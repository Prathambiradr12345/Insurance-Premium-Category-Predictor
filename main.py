"""from fastapi import FastAPI,Path,HTTPException,Query

app = FastAPI()
import json
def load_data():
    with open('patients.json','r') as f:
        data= json.load(f)
        
    return data    

@app.get('/')
def read_root():
    return {"message": "Patient Management System API"}


@app.get('/about')
def about():
    return {'Message':'A fully Functional API to manage reocrds'}


@app.get('/view')
def view():
    data=load_data()
    
    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id:str= Path(...,description="id of the patent in db",example="P001")):
    #load all the patients
    data=load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient Not Found')
@app.get('/sort')
def sort_paptients(
    sort_by: str= Query(...,description='Sort on the basis of height, weight  or bmi')
    ,order:str=Query('asc',description='Sort in asc or Desc Order')):
    valid_fields=['height','weight','bmi']
    
    if sort_by in valid_fields:
        raise HTTPException(status_code=400,detail='Invalid Fields select from {valid_field}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data=load_data
    
    sort_order=True if order=='desc' else False
    
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data
from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse



app = FastAPI()

class Patient(BaseModel):
    
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P0001'])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    
    city:Annotated[str,Field(...,description='City where the patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    
    gender:Annotated[Literal['Male','Female','Others'],Field(...,description="Gender of the patient")]

    height:Annotated[float,Field(...,gt=0,description='Height of the patient in mtr')]
    weight:Annotated[float,Field(...,gt=0,description="Height of the patient in mtr")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi<25:
            return 'normal'
        
        elif self.bmi <30:
            return 'overweight'
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]      
        
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get('/')
def read_root():
    return {"message": "Patient Management System API"}

@app.get('/about')
def about():
    return {'message': 'A fully Functional API to manage records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description="ID of the patient in DB", example="P001")
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort by height, weight, or bmi'),
    order: str = Query('asc', description='Sort order: asc or desc')
):
    valid_fields = ['height', 'weight', 'bmi']

    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field. Select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Use "asc" or "desc"')

    data = load_data()  

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )

    return sorted_data
def save_data(data):
    with open('patients.json','w')as f:
        json.dump(data,f)

@app.post('/create')
def create_patient(patient:Patient):
    #load data
    data=load_data()
    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient Already Exists")
    #new patient add to the database
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    
    #save json
    save_data(data)
    
    
    return JSONResponse(status_code=201,content={'message':'Patient create Successfully'})
    

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    
    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found")
    
    existing_patient_info=data[patient_id]
    
    update_patient_info=patient_update.model_dump(exclude_unset=True)
    
    for key,value in update_patient_info.items():
        existing_patient_info[key]=value
        
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    #-> pydatic object -> dict   
    existing_patient_info['id']=patient_id
    patient_pydantic_obj=Patient(**existing_patient_info)
    
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')
        
    # data    
    data[patient_id]=existing_patient_info    
    
    #save data
    save_data(data)
    
    
    return JSONResponse(status_code=200,content={'message':'Patient updated'})
    """
    
    
from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse
import os

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P0001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtr')]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'  # <-- added to avoid None for BMI >= 30

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]  # <-- add lt=120
    gender: Annotated[Optional[Literal['Male', 'Female', 'Others']], Field(default=None)]  # <-- align with Patient
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    # <-- safer: handle missing/corrupt file
    if not os.path.exists('patients.json'):
        return {}
    try:
        with open('patients.json', 'r') as f:
            data = json.load(f)
            # ensure dict shape
            if isinstance(data, dict):
                return data
            return {}
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=2)  # <-- pretty print

@app.get('/')
def read_root():
    return {"message": "Patient Management System API"}

@app.get('/about')
def about():
    return {'message': 'A fully Functional API to manage records'}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description="ID of the patient in DB", example="P0001")
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient Not Found')

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort by height, weight, or bmi'),
    order: str = Query('asc', description='Sort order: asc or desc')
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field. Select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Use "asc" or "desc"')

    data = load_data()

    reverse = True if order == 'desc' else False
    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse
    )
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient Already Exists")

    # store without id as value; id is the key
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'Patient created Successfully', 'id': patient.id})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    existing_patient_info = data[patient_id]
    update_patient_info = patient_update.model_dump(exclude_unset=True)

    # merge updates
    for key, value in update_patient_info.items():
        existing_patient_info[key] = value

    # Recompute bmi & verdict using Pydantic model
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient updated', 'id': patient_id})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})