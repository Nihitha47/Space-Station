from fastapi import APIRouter, HTTPException, status
from typing import List
from api.models import (
    ExperimentCreate,
    ExperimentUpdate,
    ExperimentResponse,
    ExperimentCreateResponse,
    MessageResponse,
    ErrorResponse
)
from api.database import execute_query

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.get(
    "",
    response_model=List[ExperimentResponse],
    status_code=status.HTTP_200_OK,
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_experiments():
    """
    Get all experiments with crew member names using SQL JOIN.
    
    Returns:
        List[ExperimentResponse]: List of all experiments with crew details
        
    Raises:
        HTTPException: 500 for server errors
    """
    try:
        query = """
            SELECT 
                e.experiment_id,
                e.title,
                e.status,
                e.crew_id,
                c.name as crew_name
            FROM experiment e
            INNER JOIN crew c ON e.crew_id = c.crew_id
            ORDER BY e.experiment_id DESC
        """
        
        results = execute_query(query, fetch="all")
        
        return [ExperimentResponse(**row) for row in results]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching experiments: {str(e)}"
        )


@router.post(
    "",
    response_model=ExperimentCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        404: {"model": ErrorResponse, "description": "Crew member not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_experiment(experiment: ExperimentCreate):
    """
    Create a new experiment.
    
    Args:
        experiment: ExperimentCreate model with experiment details
        
    Returns:
        ExperimentCreateResponse: Created experiment details
        
    Raises:
        HTTPException: 400 for invalid input, 404 if crew not found, 500 for server errors
    """
    try:
        # Verify crew member exists
        crew_check_query = "SELECT crew_id FROM crew WHERE crew_id = %s"
        crew_exists = execute_query(crew_check_query, (experiment.crew_id,), fetch="one")
        
        if not crew_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Crew member with ID {experiment.crew_id} not found"
            )
        
        # Insert new experiment
        insert_query = """
            INSERT INTO experiment (title, status, crew_id)
            VALUES (%s, %s, %s)
        """
        
        execute_query(
            insert_query,
            (experiment.title, experiment.status, experiment.crew_id),
            fetch="none"
        )
        
        # Get the last inserted ID
        last_id_query = "SELECT LAST_INSERT_ID() as experiment_id"
        result = execute_query(last_id_query, fetch="one")
        
        return ExperimentCreateResponse(
            experiment_id=result["experiment_id"],
            title=experiment.title,
            status=experiment.status,
            crew_id=experiment.crew_id
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating experiment: {str(e)}"
        )


@router.put(
    "/{experiment_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        404: {"model": ErrorResponse, "description": "Experiment or crew member not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def update_experiment(experiment_id: int, experiment: ExperimentUpdate):
    """
    Update an existing experiment (status, title, or crew assignment).
    
    Args:
        experiment_id: ID of the experiment to update
        experiment: ExperimentUpdate model with fields to update
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: 400 for invalid input, 404 if not found, 500 for server errors
    """
    try:
        # Check if experiment exists
        experiment_check_query = "SELECT experiment_id FROM experiment WHERE experiment_id = %s"
        experiment_exists = execute_query(experiment_check_query, (experiment_id,), fetch="one")
        
        if not experiment_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experiment with ID {experiment_id} not found"
            )
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        if experiment.title is not None:
            update_fields.append("title = %s")
            update_values.append(experiment.title)
        
        if experiment.status is not None:
            update_fields.append("status = %s")
            update_values.append(experiment.status)
        
        if experiment.crew_id is not None:
            # Verify crew member exists
            crew_check_query = "SELECT crew_id FROM crew WHERE crew_id = %s"
            crew_exists = execute_query(crew_check_query, (experiment.crew_id,), fetch="one")
            
            if not crew_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Crew member with ID {experiment.crew_id} not found"
                )
            
            update_fields.append("crew_id = %s")
            update_values.append(experiment.crew_id)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Add experiment_id to values for WHERE clause
        update_values.append(experiment_id)
        
        # Execute update
        update_query = f"""
            UPDATE experiment
            SET {', '.join(update_fields)}
            WHERE experiment_id = %s
        """
        
        execute_query(update_query, tuple(update_values), fetch="none")
        
        return MessageResponse(message=f"Experiment {experiment_id} updated successfully")
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating experiment: {str(e)}"
        )


@router.delete(
    "/{experiment_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": ErrorResponse, "description": "Experiment not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def delete_experiment(experiment_id: int):
    """
    Delete an experiment.
    
    Args:
        experiment_id: ID of the experiment to delete
        
    Returns:
        MessageResponse: Success message
        
    Raises:
        HTTPException: 404 if not found, 500 for server errors
    """
    try:
        # Check if experiment exists
        experiment_check_query = "SELECT experiment_id FROM experiment WHERE experiment_id = %s"
        experiment_exists = execute_query(experiment_check_query, (experiment_id,), fetch="one")
        
        if not experiment_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experiment with ID {experiment_id} not found"
            )
        
        # Delete experiment
        delete_query = "DELETE FROM experiment WHERE experiment_id = %s"
        execute_query(delete_query, (experiment_id,), fetch="none")
        
        return MessageResponse(message=f"Experiment {experiment_id} deleted successfully")
        
    except HTTPException:
        raise
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting experiment: {str(e)}"
        )
