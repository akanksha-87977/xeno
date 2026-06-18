from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
import shutil
from datetime import datetime

from ....core.database import get_db
from ....core.config import settings
from ....models.user import User
from ....models.validation import UploadedFile
from ....services.file_processor import FileProcessorService
from ....api.deps import get_current_active_user

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    file_type: str = "customer",  # customer or transaction
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload CSV or Excel file"""
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{file_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > settings.MAX_FILE_SIZE:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Read and preview file
    try:
        df = FileProcessorService.read_file(file_path)
        preview = FileProcessorService.preview_data(df, rows=5)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Save to database
    uploaded_file = UploadedFile(
        file_id=file_id,
        file_name=file.filename,
        file_type=file_type,
        file_path=file_path,
        row_count=len(df),
        uploaded_by=current_user.id
    )
    
    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "file_path": file_path,
        "row_count": len(df),
        "preview": preview,
        "message": "File uploaded successfully"
    }

@router.get("/history")
def get_upload_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 50
):
    """Get upload history"""
    
    files = db.query(UploadedFile).filter(
        UploadedFile.uploaded_by == current_user.id
    ).order_by(UploadedFile.uploaded_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "files": files,
        "total": db.query(UploadedFile).filter(UploadedFile.uploaded_by == current_user.id).count()
    }