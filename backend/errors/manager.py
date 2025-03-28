from fastapi import HTTPException

class ManagerNotFoundException(HTTPException):
    def __init__(self, identifier: str):
        super().__init__(status_code=404, detail=f"Manager with identifier '{identifier}' not found")