import pandas as pd
import psycopg2 as pg
from models.sensors import SensorName

# Map sensor names from a payload to their corresponding name in the db
DEVICE_TO_DB_SENSOR_NAME = {

    SensorName.ACC.value: 'acc',
    SensorName.GYRO.value: 'gyro',
    SensorName.MAG.value: 'mag'

}

def create_connection(host:str, port:str, user_name:str, password:str, database:str):

    """
    Create a Postgres database connection

    Parameters
    ----------
    host:str
        Database host
    port:str
        Database port
    user_name:str
        Database user name
    password:str
        Database password
    database:str
        Database name

    Returns
    -------
    A psycopg2 connection object
    """

    return pg.connect(user=user_name,
                      password=password,
                      host=host,
                      port=port,
                      database=database,
                      options='-c statement_timeout=300000')

def get_recent_triaxial_data(connection:pg.connect,
                             table_name:str,
                             sensor_name:str,
                             sample_rate:int,
                             num_seconds:float,
                             max_lookback_seconds:float):

    """
    Query the most recent data from a triaxial smartphone sensor.

    Parameters
    ----------
    connection:pg.connect
        A postgres connection object
    table_name:str
        The table where the sensor data is stored
    sensor_name:str
        The name of the sensor to query
    sample_rate:int
        The sampling rate of the sensor (in hz)
    num_seconds:float
        The number of seconds of data to pull
    max_lookback_seconds:float
        The maximum amount seconds to look for data from.
        For instance, if a device stopped producing data
        10 seconds ago, and max_lookback_seconds = 10,
        then data for this device will be ignored.

    Returns
    -------
    A DataFrame with the requested sensor data
    """

    # The number of samples to get
    num_samples:int = int(sample_rate*num_seconds)

    query:str = f"""with tmp as (select device_id,
                                       recorded_timestamp,
                                       x,
                                       y,
                                       z,
                                       row_number() over(partition by device_id order by
                                                        recorded_timestamp desc) as rn
                                        from {table_name}
                                        where sensor_name = '{sensor_name}'
                                        and recorded_timestamp::timestamp >= dateadd('s', -{int(max_lookback_seconds)}, now())
                               )

                              select * from tmp 
                              where rn <= {num_samples}
                              """

    return pd.read_sql(query, connection)





    



