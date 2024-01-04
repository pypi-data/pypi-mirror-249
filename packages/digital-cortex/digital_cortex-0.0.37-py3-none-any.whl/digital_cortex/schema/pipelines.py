from typing import Optional

from pydantic import BaseModel


class EtlPipelineForm(BaseModel):
    name: str
    pipelineTypeId: str
    sourceDatasetId: str
    targetDatasetId: str
    functionId: str
    isPublished: bool


class UpdateEtlPipelineForm(BaseModel):
    id: str
    sourceDatasetId: str
    targetDatasetId: str
    functionId: str


class UpdatePipelineDescriptionForm(BaseModel):
    id: str
    description: str


class UpdatePipelineGeneralFieldsForm(BaseModel):
    id: str
    name: str
    subtitle: Optional[str] = None
