import os
from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


APP_NAME = os.getenv("APP_NAME", "Employee Leave Management")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


class LeaveStatus(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"


class LeaveCreate(BaseModel):
    employee_name: str = Field(min_length=2, max_length=100)
    leave_type: str = Field(min_length=2, max_length=50)
    start_date: date
    end_date: date
    reason: str = Field(min_length=3, max_length=500)


class LeaveRecord(LeaveCreate):
    id: int
    status: LeaveStatus


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Simple Employee Leave Management API",
)


leave_requests: list[LeaveRecord] = [
    LeaveRecord(
        id=1,
        employee_name="Demo Employee",
        leave_type="Casual Leave",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 8, 2),
        reason="Personal work",
        status=LeaveStatus.pending,
    )
]


@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "environment": APP_ENV,
        "version": APP_VERSION,
        "message": "Employee Leave Management API is running",
        "documentation": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/api/leaves", response_model=list[LeaveRecord])
def list_leaves():
    return leave_requests


@app.get("/api/leaves/{leave_id}", response_model=LeaveRecord)
def get_leave(leave_id: int):
    for leave in leave_requests:
        if leave.id == leave_id:
            return leave

    raise HTTPException(status_code=404, detail="Leave request not found")


@app.post("/api/leaves", response_model=LeaveRecord, status_code=201)
def create_leave(request: LeaveCreate):
    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date",
        )

    new_leave = LeaveRecord(
        id=max((leave.id for leave in leave_requests), default=0) + 1,
        **request.model_dump(),
        status=LeaveStatus.pending,
    )

    leave_requests.append(new_leave)
    return new_leave


@app.patch("/api/leaves/{leave_id}/approve", response_model=LeaveRecord)
def approve_leave(leave_id: int):
    for leave in leave_requests:
        if leave.id == leave_id:
            leave.status = LeaveStatus.approved
            return leave

    raise HTTPException(status_code=404, detail="Leave request not found")


@app.patch("/api/leaves/{leave_id}/reject", response_model=LeaveRecord)
def reject_leave(leave_id: int):
    for leave in leave_requests:
        if leave.id == leave_id:
            leave.status = LeaveStatus.rejected
            return leave

    raise HTTPException(status_code=404, detail="Leave request not found")
