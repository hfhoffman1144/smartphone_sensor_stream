from enum import Enum

class SensorName(Enum):

    """
    An enum class representing the names of smartphone sensors
    """
    
    ACC = 'accelerometeruncalibrated'
    GYRO = 'gyroscopeuncalibrated'