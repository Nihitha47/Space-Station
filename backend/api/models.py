from pydantic import BaseModel, Field
from typing import Optional


# ===========================
# Authentication Models
# ===========================

class LoginRequest(BaseModel):
    """Request model for crew login"""
    crew_id: int = Field(..., description="Crew member ID")
    password: str = Field(..., description="Crew member password")


class LoginResponse(BaseModel):
    """Response model for successful login"""
    crew_id: int
    name: str
    role: str
    nationality: str
    message: str = "Login successful"


# ===========================
# Crew Models
# ===========================

class CrewMember(BaseModel):
    """Crew member model"""
    crew_id: int
    name: str
    role: str
    nationality: str


# ===========================
# Mission Models
# ===========================

class MissionCreate(BaseModel):
    """Request model for creating a mission"""
    name: str = Field(..., min_length=1, max_length=255)
    purpose: str = Field(..., min_length=1, max_length=500)
    crew_id: int = Field(..., description="Assigned crew member ID")


class MissionUpdate(BaseModel):
    """Request model for updating a mission"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    purpose: Optional[str] = Field(None, min_length=1, max_length=500)
    crew_id: Optional[int] = Field(None, description="Assigned crew member ID")


class MissionResponse(BaseModel):
    """Response model for mission data"""
    mission_id: int
    name: str
    purpose: str
    crew_id: int
    crew_name: str = Field(..., description="Name of assigned crew member")


class MissionCreateResponse(BaseModel):
    """Response model for mission creation"""
    mission_id: int
    name: str
    purpose: str
    crew_id: int
    message: str = "Mission created successfully"


# ===========================
# Experiment Models
# ===========================

class ExperimentCreate(BaseModel):
    """Request model for creating an experiment"""
    title: str = Field(..., min_length=1, max_length=255)
    status: str = Field(..., min_length=1, max_length=100)
    crew_id: int = Field(..., description="Assigned crew member ID")


class ExperimentUpdate(BaseModel):
    """Request model for updating an experiment"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = Field(None, min_length=1, max_length=100)
    crew_id: Optional[int] = Field(None, description="Assigned crew member ID")


class ExperimentResponse(BaseModel):
    """Response model for experiment data"""
    experiment_id: int
    title: str
    status: str
    crew_id: int
    crew_name: str = Field(..., description="Name of assigned crew member")


class ExperimentCreateResponse(BaseModel):
    """Response model for experiment creation"""
    experiment_id: int
    title: str
    status: str
    crew_id: int
    message: str = "Experiment created successfully"


# ===========================
# Generic Response Models
# ===========================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
