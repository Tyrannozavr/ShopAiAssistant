from fastapi import APIRouter, HTTPException, UploadFile, Form
from typing import List

router = APIRouter()

@router.post("/photo")
async def process_photo(
    photo: UploadFile,
    door_type: str = Form(...),
    priorities: List[str] = Form(...),
    user_request: str = Form(...)
):
    # Mocked response for processing a photo
    try:
        # Simulate processing logic
        return {"message": "Photo processed successfully", "details": {
            "door_type": door_type,
            "priorities": priorities,
            "user_request": user_request
        }}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process photo: {str(e)}")