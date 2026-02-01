from fastapi import APIRouter, HTTPException, status
from typing import List
from api.models import (
    MissionCreate,
    MissionUpdate,
    MissionResponse,
    MissionCreateResponse,
    MessageResponse,
    ErrorResponse
)
from api.database import execute_query

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.get(
    "",
    response_model=List[MissionResponse],
    status_code=status.HTTP_200_OK,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_missions():
    """
    Get all missions with crew member names using SQL JOIN.
    
    Returns:
        List[MissionResponse]: List of all missions with crew details
        
    Raises:
        HTTPException: 500 for server errors
    """
    try:
        query = """
            SELECT 
                m.mission_id,
                m.name,
                m.purpose,
                m.crew_id,
                c.name as crew_name
            FROM mission m
            INNER JOIN crew c ON m.crew_id = c.crew_id
            ORDER BY m.mission_id DESC
        """
        
        results = execute_query(query, fetch="all")
        
        return [MissionResponse(**row) for row in results]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching missions: {str(e)}"
        )


@router.post(
    "",
    response_model=MissionCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        404: {"model": ErrorResponse, "description": "Crew member not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_mission(mission: MissionCreate):
    """
    Create a new mission.
    
    Args:
        mission: MissionCreate model with mission details
        
    Returns:
        MissionCreateResponse: Created mission details
        
    Raises:
        HTTPException: 400 for invalid input, 404 if crew not found, 500 for server errors
    """
    try:
        # Verify crew member exists
        crew_check_query = "SELECT crew_id FROM crew WHERE crew_id = %s"
        crew_exists = execute_query(crew_check_query, (mission.crew_id,), fetch="one")
        
        if not crew_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Crew member with ID {mission.crew_id} not found"
            )
        
        # Insert new mission
        insert_query = """
            INSERT INTO mission (name, purpose, crew_id)
            VALUES (%s, %s, %s)
        """
        
        execute_query(
            insert_query,
            (mission.name, mission.purpose, mission.crew_id),
            fetch="none"
        )
        
        # Get the last inserted ID
        last_id_query = "SELECT LAST_INSERT_ID() as mission_id"
        result = execute_query(last_id_query, fetch="one")
        
        return MissionCreateResponse(
            mission_id=result["mission_id"],
            name=mission.name,
            purpose=mission.purpose,
            crew_id=mission.crew_id
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating mission: {str(e)}"
        )


@router.put(
    "/{mission_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        404: {"model": ErrorResponse, "description": "Mission or crew member not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def update_mission(mission_id: int, mission: MissionUpdate):
    """
    Update an existing mission.
    
    Args:
        mission_id: ID of the mission to update
        mission: MissionUpdate model with fields to update
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: 400 for invalid input, 404 if not found, 500 for server errors
    """
    try:
        # Check if mission exists
        mission_check_query = "SELECT mission_id FROM mission WHERE mission_id = %s"
        mission_exists = execute_query(mission_check_query, (mission_id,), fetch="one")
        
        if not mission_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with ID {mission_id} not found"
            )
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if mission.name is not None:
            update_fields.append("name = %s")
            update_values.append(mission.name)
        
        if mission.purpose is not None:
            update_fields.append("purpose = %s")
            update_values.append(mission.purpose)
        
        if mission.crew_id is not None:
            # Verify crew member exists
            crew_check_query = "SELECT crew_id FROM crew WHERE crew_id = %s"
            crew_exists = execute_query(crew_check_query, (mission.crew_id,), fetch="one")
            
            if not crew_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Crew member with ID {mission.crew_id} not found"
                )
            
            update_fields.append("crew_id = %s")
            update_values.append(mission.crew_id)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Add mission_id to values for WHERE clause
        update_values.append(mission_id)
        
        # Execute update
        update_query = f"""
            UPDATE mission
            SET {', '.join(update_fields)}
            WHERE mission_id = %s
        """
        
        execute_query(update_query, tuple(update_values), fetch="none")
        
        return MessageResponse(message=f"Mission {mission_id} updated successfully")
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating mission: {str(e)}"
        )


@router.delete(
    "/{mission_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Mission not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_mission(mission_id: int):
    """
    Delete a mission.
    
    Args:
        mission_id: ID of the mission to delete
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: 404 if not found, 500 for server errors
    """
    try:
        # Check if mission exists
        mission_check_query = "SELECT mission_id FROM mission WHERE mission_id = %s"
        mission_exists = execute_query(mission_check_query, (mission_id,), fetch="one")
        
        if not mission_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with ID {mission_id} not found"
            )
        
        # Delete mission
        delete_query = "DELETE FROM mission WHERE mission_id = %s"
        execute_query(delete_query, (mission_id,), fetch="none")
        
        return MessageResponse(message=f"Mission {mission_id} deleted successfully")
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting mission: {str(e)}"
        )
