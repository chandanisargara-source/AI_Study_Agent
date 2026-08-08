from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user, require_role
from auth.permissions import admin_required
from database.database import get_db
from models.user import User

print("USER ROUTER LOADED")

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def get_profile(current_user=Depends(get_current_user)):
    return current_user


@router.get("/all")
def get_all_users(
    admin_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    return users

@router.get("/student-dashboard")
def student_dashboard(
    current_user=Depends(require_role("student"))
):
    return {
        "name": current_user.name,
        "role": current_user.role,
        "dashboard": {
            "features": [
                "AI Notes Generator",
                "AI Quiz Generator",
                "AI Doubt Solver",
                "AI Study Planner"
            ],
            "progress": "0%"
        }
    }

@router.get("/teacher-dashboard")
def teacher_dashboard(
    current_user=Depends(require_role("teacher"))
):
    return {
        "name": current_user.name,
        "role": current_user.role,
        "dashboard": {
            "features": [
                "AI Assignment Checker",
                "AI Question Paper Generator",
                "Student Performance Dashboard",
                "Class Analytics"
            ],
            "students": 0
        }
    }

@router.get("/admin-dashboard")
def admin_dashboard(
    current_user=Depends(require_role("admin"))
):
    return {
        "name": current_user.name,
        "role": current_user.role,
        "dashboard": {
            "features": [
                "User Management",
                "Student Analytics",
                "System Reports",
                "Platform Management"
            ],
            "total_users": 0
        }
    }