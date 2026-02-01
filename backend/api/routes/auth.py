from fastapi import APIRouter, HTTPException, status
from api.models import LoginRequest, LoginResponse, ErrorResponse
from api.database import execute_query

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post(
    "",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def login(credentials: LoginRequest):
    """
    Authenticate crew member with crew_id and password.
    
    Args:
        credentials: LoginRequest containing crew_id and password
        
    Returns:
        LoginResponse: Crew member details (without password)
        
    Raises:
        HTTPException: 401 if credentials are invalid, 500 for server errors
    """
    try:
        # Query to validate credentials
        query = """
            SELECT crew_id, name, role, nationality, password
            FROM crew
            WHERE crew_id = %s
        """
        
        result = execute_query(query, (credentials.crew_id,), fetch="one")
        
        # Check if crew member exists
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid crew ID or password"
            )
        
        # Validate password (plain text comparison)
        # Note: In production, use hashed passwords with bcrypt or similar
        if result["password"] != credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid crew ID or password"
            )
        
        # Return crew details without password
        return LoginResponse(
            crew_id=result["crew_id"],
            name=result["name"],
            role=result["role"],
            nationality=result["nationality"]
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Handle database or other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )
