from __future__ import annotations

import calendar
import datetime
import io
import re
from dataclasses import InitVar
from decimal import Decimal
from re import Pattern
from typing import Annotated, Any, Optional

import bcrypt
from ormspace import functions
from ormspace.bases import AbstractRegex
from spacestar.model import SpaceModel
from ormspace.model import modelmap, SearchModel
from ormspace.annotations import PasswordField, DateField, TitleField, MultiLineTextField
from ormspace.enum import Gender, StrEnum
from pydantic import AfterValidator, computed_field, EmailStr, Field, field_validator
from typing_extensions import Self

from detadoc.regex import ActiveDrug, Package, ProfessionalId


class CreationBase(SpaceModel):
    creator: User.Key = Field('admin')
    created: DateField
    
    
class EmailBase(SpaceModel):
    email: EmailStr
    
    @classmethod
    async def get_by_email(cls, email: str) -> Optional[User]:
        if data:= await cls.instances_list(query={'email': email}):
            assert len(data) == 1
            return data[0]
        return None
    
    
@modelmap
class User(CreationBase, EmailBase):
    EXIST_QUERY = 'email'
    password: PasswordField
    
    @classmethod
    async def get_and_check(cls, email: str, password: str) -> Optional[User]:
        user = await cls.get_by_email(email)
        if user:
            if user.check(password):
                return user
        return None
    
    @classmethod
    def create_encrypted(cls, email: str, password: str) -> Self:
        return cls(email=email, password=cls.encrypt_password(password))
    
    @classmethod
    def encrypt_password(cls, password: str) -> bytes:
        return bcrypt.hashpw(functions.str_to_bytes(password), bcrypt.gensalt())
    
    def check(self, password: str) -> bool:
        return bcrypt.checkpw(functions.str_to_bytes(password), self.password)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and self.email == other.email
    
    def __hash__(self):
        return hash(self.email)
    
@modelmap
class Admin(User):
    TABLE_NAME = 'User'
    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        self.key = 'admin'
        
    async def profile(self):
        result = await Profile.instances_list(query={'email': self.email})
        if result:
            return result[0]
        return
    
    
class Person(SearchModel):
    EXIST_QUERY = ['code', 'cpf']
    fname: TitleField
    lname: TitleField
    gender: Gender
    bdate: DateField
    cpf: Optional[str] = None
    sname: Optional[str] = None
    
    def __str__(self):
        return self.sname if self.sname else ' '.join([self.fname, self.lname])
    
    @property
    def age(self):
        return functions.years(datetime.date.today(), self.bdate)
    
    # noinspection PyNestedDecorators
    @field_validator('cpf')
    @classmethod
    def _cpf_validator(cls, v: str) -> str:
        if v:
            digits = ''.join(functions.find_digits(v))
            if len(digits) != 11:
                raise ValueError('CPF deve ter 11 digitos')
            return digits
        return v

    @computed_field
    @property
    def code(self) -> str:
        with io.StringIO() as f:
            f.write(self.bdate.isoformat().replace('-', ''))
            f.write(self.gender.name)
            f.write(self.fname[:2])
            f.write(self.lname.split()[-1][:2])
            return f.getvalue().upper()
    
    
class Contact(SpaceModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    
    # noinspection PyNestedDecorators
    @field_validator('phone')
    @classmethod
    def _phone_validator(cls, v: str) -> str:
        if v:
            digits = ''.join(re.findall(r'\+|\d', v))
            return digits
        return v
    
class Profile(Person, Contact):
    ...
    
class Staff(Profile):
    cpf: str
    phone: str
    email: EmailStr
    address: str
    city: str


class Professional(Staff):
    professional_id: ProfessionalId
    specialties: list[str] = Field(default_factory=list)
    subspecialties: list[str] = Field(default_factory=list)
    
    
@modelmap
class Doctor(Professional):
    MODEL_GROUPS = ['Profile', 'Staff', 'Professional']




@modelmap
class Therapist(Professional):
    ...

@modelmap
class Patient(Profile):
    MODEL_GROUPS = ['Profile']


@modelmap
class Employee(Staff):
    MODEL_GROUPS = ['Profile', 'Staff']
    salary: Decimal
    start: datetime.date
    month_days: int
    day_hours: float
    
    
class Medication(SearchModel):
    label: Optional[str] = Field(None)
    drugs: list[ActiveDrug]
    class Route(StrEnum):
        O = 'Oral'
        P ='Parenteral'
        T = 'Tópica'
        F = 'Oftalmológica'
        N = 'Nasal'
        A = 'Otoscópica'
        R = 'Retal'
        
    route: Route = Field(Route.O)
    
    class DosageForm(StrEnum):
        TAB = 'Comprimido'
        CAP = 'Cápsula'
        PAT = 'Adesivo'
        LIQ = 'Líquido'
        STR = 'Strip'
        POW = 'Pó'
        PAS = 'Pasta'
        DRO = 'Gota'
        AER = 'Aerosol'
        
    dosage_form: DosageForm
    package: Package
    pharmaceutical: Optional[str] = Field(None)
    
    def __eq__(self, other):
        return isinstance(other, type(self)) and str(self) == str(other)
    
    def __hash__(self):
        return hash(str(self))
    
    @property
    def is_generic(self):
        return self.label is None
    
    @property
    def is_single_drug(self):
        return len(self.drugs) == 1
    
    @property
    def package_content(self):
        return getattr(self.package, 'content', None)
    
    @property
    def package_size(self):
        return functions.parse_number(getattr(self.package, 'size', None))

    @property
    def drug_names(self):
        return functions.join([getattr(i, 'name') for i in self.drugs], sep=" + ")
    
    @property
    def drug_strengths(self):
        return functions.join([f"{getattr(i, 'strength')}{getattr(i, 'unit')}" for i in self.drugs], sep=" + ")
    
    def __str__(self):
        if not self.is_generic:
            return f'{self.label} ({self.drug_names}) {self.drug_strengths} {self.package}'
        return f'{self.drug_names.title()} {self.drug_strengths} {self.package}'

@modelmap
class Event(SpaceModel):
    patient_key: Patient.Key
    creator: Optional[User.Key] = None
    title: str
    notes: Optional[str] = Field(None)
    age: Optional[float] = Field(None, exclude=True)
    date: Optional[datetime.date] = Field(None)
    
    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        if not self.age and not self.date:
            raise ValueError('age or date is required for Event')
        if self.age and not self.date:
            if self.patient_key.instance:
                days = datetime.timedelta(days=int(self.age * 365))
                date = self.patient_key.instance.bdate + days
                self.date = date + calendar.leapdays(self.patient_key.instance.bdate.year, date.year)
    
