import sqlite3
from contextlib import closing
from typing import Optional
from uuid import UUID

from Hospital_System.domain.entities import Patient
from Hospital_System.domain.interface.repository import PatientRecord
from Hospital_System.domain.value_object import (
    NationalID, PhoneNumber, Name, Address, Rights, PatientRights, DateOfBirth )


class SqlPatientRecord(PatientRecord):
    _CREATE_SCHEMA_QUERY = """
        CREATE TABLE IF NOT EXISTS patient (
        id TEXT PRIMARY KEY,
        national_id TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT,
        date_of_birth TEXT,
        registered_address TEXT,
        current_address TEXT,
        rights TEXT
        )
    """

    _UPSERT_PATIENT_QUERY = """
    INSERT INTO patient (
        id, national_id, first_name, last_name, 
        phone_number, date_of_birth, registered_address, 
        current_address, rights)
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    _SELECT_BY_NATIONAL_ID_QUERY = """
        SELECT * FROM patient WHERE national_id = ?
    """


    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._auto_create_schema()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _auto_create_schema(self) -> None:
        with closing(self._get_connection()) as conn:
            with conn:
                conn.execute(self._CREATE_SCHEMA_QUERY)

    def save(self, patient: Patient) -> None:
        with closing(self._get_connection()) as conn:
            with conn:
                data = self._map_entity_to_tuple(patient)
                conn.execute(self._UPSERT_PATIENT_QUERY, data)

    def get_by_national_id(self, national_id: NationalID) -> Optional[Patient]:
        with closing(self._get_connection()) as conn:
            row = conn.execute(self._SELECT_BY_NATIONAL_ID_QUERY, (str(national_id.id),)).fetchone()
            if row is not None:
                return self._map_row_to_entity(row)
            return None

    def _map_row_to_entity(self, row: sqlite3.Row) -> Patient:
        return Patient(
            id=UUID(row['id']),
            national_id=NationalID(id=row['national_id']),
            first_name=Name(value=row['first_name']),
            last_name=Name(value=row['last_name']),
            phone_number=PhoneNumber(value=row['phone_number']),
            date_of_birth=DateOfBirth.model_validate_json(row['date_of_birth']),
            registered_address=Address.model_validate_json(row['registered_address']),
            current_address=Address.model_validate_json(row['current_address']),
            rights=Rights(rights_type=PatientRights(row['rights']))
        )

    def _map_entity_to_tuple(self, patient: Patient) -> tuple[str, str, str, str, str, str, str, str, str]:
        data = (
            str(patient.id),
            patient.national_id.id,
            patient.first_name.value,
            patient.last_name.value,
            patient.phone_number.value,
            patient.date_of_birth.model_dump_json(),
            patient.registered_address.model_dump_json(),
            patient.current_address.model_dump_json(),
            patient.rights.rights_type.value,
        )
        return data

