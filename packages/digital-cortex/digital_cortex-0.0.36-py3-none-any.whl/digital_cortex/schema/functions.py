from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CodeType(str, Enum):
    file = "file"
    text = "text"


class DependencyType(str, Enum):
    file = "file"
    text = "text"


class FunctionForm(BaseModel):
    name: str
    computeTypeId: str
    codeType: CodeType
    code: Optional[str] = None
    dependencyType: Optional[DependencyType] = None
    dependency: Optional[str] = None
    isPublished: bool



class UpdateFunctionCodeForm(BaseModel):
    id: str
    code: str


class UpdateFunctionDependencyForm(BaseModel):
    id: str
    dependencyType: DependencyType
    dependency: Optional[str] = None


class UpdateFunctionDescriptionForm(BaseModel):
    id: str
    description: str


class UpdateFunctionGeneralFieldsForm(BaseModel):
    id: str
    name: str
    subtitle: Optional[str] = None
    version: Optional[str] = None
