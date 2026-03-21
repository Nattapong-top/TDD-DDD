from uuid import UUID

from pydantic import BaseModel, ConfigDict

from Hospital_System.domain.value_object import (
    Name, PhoneNumber, DateOfBirth, Address, NationalID, Rights)


class DomainEntity(BaseModel):
    model_config = ConfigDict(frozen=False)


class Patient(DomainEntity):
    id: UUID
    nation_id: NationalID
    first_name: Name
    last_name: Name
    phone_number: PhoneNumber
    date_of_birth: DateOfBirth
    registered_address: Address
    current_address: Address
    right: Rights
