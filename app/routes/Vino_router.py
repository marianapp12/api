from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException, Query, Response
from starlette import status

from app.config.db import db
from app.core.utils import serialize_doc, get_document_or_404, dict_to_xml
from app.entities.Vino import Vino, VinoInDB

name_router = 'Vino'
Vino_router = APIRouter(prefix=f'/{name_router}', tags=[name_router])
cursor = db.get_collection(name_router)


@Vino_router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_vino(Vino: Vino):
    """
    Create a new Vino in the database.

    **Requires**: An `Vino` object containing the Vino's details.
    **Returns**: A dictionary with the newly created Vino's ID.

    - **Status Code 201**: Vino created successfully.
    - **Status Code 422**: Invalid input validation error.
    """
    try:
        result = cursor.insert_one(Vino.dict())
        document_id = result.inserted_id
        return {"_id created": str(document_id)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error creating Vino: {str(e)}")


@Vino_router.get("/{Vino_id}", status_code=status.HTTP_200_OK)
async def get_Vino_by_id(Vino_id: str, format: str = Query("json", enum=["json", "xml"])):
    """
    Retrieve an Vinor by their ID.

    **Requires**: A valid `Vino_id`.
    **Returns**: The Vino's details.

    - **Status Code 200**: Vino found and returned.
    - **Status Code 400**: Invalid ID format.
    - **Status Code 404**: Vino not found.
    """

    # Retrieve Vino from database
    Vino = get_document_or_404(cursor, Vino_id, "Vino")

    # Serialize document
    Vino_data = serialize_doc(Vino, VinoInDB).dict()

    # Return response in the specified format
    if format == "xml":
        Vino_data_xml = dict_to_xml("Vino", Vino_data)
        return Response(content=Vino_data_xml, media_type="application/xml")

    # Return serialized Vino document
    return Vino_data


@Vino_router.get("/", status_code=status.HTTP_200_OK)
async def get_Vinos(skip: int = 0, limit: int = 10, format: str = Query("json", enum=["json", "xml"])):
    """
    Retrieve a list of Vinos with pagination.

    **Requires**: `skip` (offset) and `limit` (number of results) for pagination.
    **Returns**: A list of Vinos.

    - **Status Code 200**: Vinos list returned successfully.
    - **Status Code 500**: Server error while retrieving Vinos.
    """
    try:
        Vinos = cursor.find().skip(skip).limit(limit)
        Vino_list = [serialize_doc(Vino, VinoInDB).dict() for Vino in Vinos]

        if format == "xml":
            # Convert each Vino dict to XML
            Vinos_data_xml = "<Vino>"
            for Vino_data in Vino_list:
                Vinos_data_xml += dict_to_xml("Vino", Vino_data)
            Vinos_data_xml += "</Vino>"
            return Response(content=Vinos_data_xml, media_type="application/xml")

        return Vino_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving Vinos: {str(e)}")


@Vino_router.put("/{Vino_id}", response_model=VinoInDB, status_code=status.HTTP_200_OK)
async def update_Vino(Vino_id: str, Vino: Vino):
    """
    Update an Vino's details.

    **Parameters**:
    - **Vino_id** (str): Unique ID of the Vino to be updated.
    - **Vino** (Vino): Object containing the new details of the Vino.

    **Returns**:
    - **VinoInDB**: Updated Vino data.

    **Status Codes**:
    - **200 OK**: Vino updated successfully.
    - **404 Not Found**: Vino with the given ID not found.
    - **500 Internal Server Error**: Error occurred while updating the Vino.
    """
    try:

        # Attempt to update the Vino
        cursor.update_one({"_id": ObjectId(Vino_id)}, {"$set": Vino.dict()})

        # Retrieve the updated Vino
        updated_Vino = cursor.find_one({"_id": ObjectId(Vino_id)})

        # Return the updated Vino
        return serialize_doc(updated_Vino, VinoInDB)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error updating Vino: {str(e)}")


@Vino_router.delete("/{Vino_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_Vino(Vino_id: str):
    """
    Delete an Vino by their ID.

    **Parameters**:
    - **Vino_id** (str): Unique ID of the Vino to be deleted.

    **Returns**:
    - A message indicating the result of the operation.

    **Status Codes**:
    - **200 OK**: Vino deleted successfully.
    - **404 Not Found**: Vino with the given ID not found.
    """
    try:

        # Attempt to delete the Vino
        cursor.delete_one({"_id": ObjectId(Vino_id)})

        return {"detail": "Vino deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error deleting Vino: {str(e)}")
