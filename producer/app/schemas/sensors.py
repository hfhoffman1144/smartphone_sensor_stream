from pydantic import BaseModel, validator
from datetime import datetime
from typing import List, Dict, Union


class SensorReading(BaseModel):

    """
    Base model class for incoming requests from smartphone sensors

    Attributes
    ----------
    messageId : int
        The identifier of a message in the current session
    sessionId : int
        The identifier of a session
    deviceId : int
        The identifier of the device sending the data
    payload : List[Dict[str:Union[str, int, Dict]]]
        The payload of the request containing sensor readings
        and metadata about the readings
    """

    messageId: int
    sessionId: str
    deviceId: str
    payload: List[Dict[str, Union[str, int, Dict]]]
    
class SensorResponse(BaseModel):

    """
    Base model class for the response of the sensor request endpoint

    Attributes
    ----------
    messageId : int
        The identifier of a message in the current session
    sessionId : int
        The identifier of a session
    deviceId : int
        The identifier of the device sending the data
    timestamp : str
        The timestamp when a sensor request was processed
    """
    messageId: str
    sessionId: str
    deviceId: str
    timestamp: str = ""

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())