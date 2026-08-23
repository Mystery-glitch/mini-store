from typing import Annotated

from fastapi import Depends,APIRouter,BackgroundTasks
from app.dependencies.auth import get_current_user
from app.models.user import User

router=APIRouter(prefix="/users",tags=["Users"])

def write_notification(email:str,message:str):
    with open("notification.log","a",encoding="utf-8") as file:
        file.write(f"{email}; {message}")

@router.post("/notify")
def notify(background_tasks:BackgroundTasks,current_user:Annotated[User,Depends(get_current_user)]):
    background_tasks.add_task(write_notification,current_user.email,"Welcome to Mini store!!")

    return {
        "message":"Notification schedule"
    }