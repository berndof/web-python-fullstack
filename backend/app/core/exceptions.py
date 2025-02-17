from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, error_code: str, message: str, status_code: int):
        super().__init__(status_code=status_code, detail={"error_code": error_code, "message": message})


class UserAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            error_code="USER_ALREADY_EXISTS", message="User already exists", status_code=status.HTTP_400_BAD_REQUEST
        )


class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__(error_code="USER_NOT_FOUND", message="User not found", status_code=status.HTTP_404_NOT_FOUND)
