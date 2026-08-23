from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter,File,UploadFile
from fastapi.responses import FileResponse

router=APIRouter(prefix="/files",tags=["Files"])

UPLOAD_DIR=Path("app/static/uploads")
UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

@router.post("/upload")
async def upload_file(file:UploadFile=File(...)):
    extension=Path(file.filename or "").suffix
    filename=f"{uuid4()}{extension}"
    destination=UPLOAD_DIR/filename
    with destination.open("wb") as buffer:
        while chunk:= await file.read(1024*1024):
            buffer.write(chunk)

    return {
        "filename":filename,
        "original_filename":file.filename,
        "content_type":file.content_type
    }

@router.get("/{filename}")
def download_file(filename:str):
    path=UPLOAD_DIR/filename
    return FileResponse(path,filename=filename)