import pandas as pd
import sqlite3
from app.data.db import connect_database

def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """Insert new incident."""
    cursor = conn.cursor()
    insert_sql = """
                   INSERT INTO cyber_incidents
                   (date, incident_type, severity, status, description, reported_by)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """ 
    cursor.execute(
        insert_sql,
        (date, incident_type, severity, status, description, reported_by)
    )             
    return cursor.lastrowid

def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.
    
    TODO: Implement using pandas.read_sql_query()
    
    Returns:
        pandas.DataFrame: All incidents
    """
    # TODO: Use pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    try: 
        df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
        return df
    except Exception as e:
        print(f"Error retrieving incidents: {e}")
        return pd.DataFrame()
pass
def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    
    TODO: Implement UPDATE operation.
    """
    # TODO: Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE id = ?
    try:
        update_sql = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
        """
    # TODO: Execute and commit
        conn.execute(update_sql, (new_status, incident_id))
        conn.commit() 
    # TODO: Return cursor.rowcount
        cursor = conn.cursor()
        return cursor.rowcount
    except Exception as e:
        print(f"Error updating incident status: {e}")
        return 0   
pass
def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    
    TODO: Implement DELETE operation.
    """
    # TODO: Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    try:
        delete_sql = """ 
        DELETE FROM  cyber_incidents
        WHERE id = ?
        """
    # TODO: Execute and commit
        conn.execute(delete_sql, (incident_id,))
        conn.commit()
    # TODO: Return cursor.rowcount
        cursor = conn.cursor()
        return cursor.rowcount
    except Exception as e:
        print(f"Error deleting incident: {e}")
        return 0
pass

