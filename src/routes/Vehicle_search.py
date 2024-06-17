from fastapi import APIRouter, HTTPException
import psycopg2

router = APIRouter(prefix="/vehicle_search", tags=['vehicle_search'])


@router.post("/find-parking-sessions/")
async def find_parking_sessions(license_plate: str):
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='db3',
            user='postgres',
            password='567234'
        )
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM vehicles WHERE license_plate = %s", (license_plate,))
        vehicle_id = cursor.fetchone()

        if vehicle_id is None:
            raise HTTPException(status_code=404, detail="Vehicle not found")

        vehicle_id = vehicle_id[0]

        cursor.execute("SELECT * FROM parking_sessions WHERE id = %s", (vehicle_id,))
        parking_sessions = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]

        cursor.close()
        connection.close()

        if not parking_sessions:
            return {"message": "No parking sessions found for the given vehicle ID"}

        parking_sessions_with_columns = [
            dict(zip(column_names, session)) for session in parking_sessions
        ]

        return {"parking_sessions": parking_sessions_with_columns}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
