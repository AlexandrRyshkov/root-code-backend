import os
from dotenv import load_dotenv

load_dotenv()
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.railway_line import RailwayLine
from models.railway_line_stations import RailwayLineStation
from models.station import Station

engine = create_engine(os.getenv('DATABASE_CONNECTION_STRING'))
Session = sessionmaker(bind=engine)
session = Session()


def get_stations(df):
    stations = {}
    for index, row in df.iterrows():
        start_station = row["NAME_BEGIN_MELK_SET":"OKATO_BEGIN_MELK_SET_NAME"]
        end_station = row["NAME_END_MELK_SET":"OKATO_END_MELK_SET_NAME"]
        stations[row["ESR_BEGIN_MELK_SET"]] = Station(name=start_station[0], esr_code=start_station[1],
                                                      railroad_code=start_station[2], okato_name=start_station[3])
        stations[row["ESR_END_MELK_SET"]] = Station(name=end_station[0], esr_code=end_station[1],
                                                    railroad_code=end_station[2], okato_name=end_station[3])
    return stations


def load_railway_line(railway_line):
    session.add(railway_line)
    session.flush()
    return railway_line


def load_stations(stations):
    result = []
    for key, value in stations.items():
        session.add(value)
        session.flush()
        result.append(value)
    return result


def load_railway_lines(df, stations):
    stations_ids = {}
    for station in stations:
        stations_ids[station.esr_code] = station.id

    railway_line = RailwayLine()
    for index, row in df.iterrows():
        stop_number = row["NUM_CNSI_MELK_SET"]
        start_station_esr = row["ESR_BEGIN_MELK_SET"]
        end_station_esr = row["ESR_END_MELK_SET"]

        if stop_number == 1:
            start_station_id = stations_ids[row["ESR_BEGIN_VOST_UCH"]]
            start_station_x_y = {'x': row["X_BEG_VOST_UCH"], 'y': row["Y_BEG_VOST_UCH"]}

            session.query(Station).filter(Station.id == start_station_id).update(start_station_x_y)

            end_station_id = stations_ids[row["ESR_END_VOST_UCH"]]
            end_station_x_y = {'x': row["X_END_VOST_UCH"], 'y': row["Y_END_VOST_UCH"]}

            session.query(Station).filter(Station.id == end_station_id).update(end_station_x_y)

        if index > 0:
            load_railway_line(railway_line)
            railway_line = RailwayLine()

    railway_line.stations.append(RailwayLineStation(start_station_id=stations_ids[start_station_esr],
                                                    end_station_id=stations_ids[end_station_esr],
                                                    stop_number=stop_number))


def main():
    try:
        df = pd.read_excel(os.getenv('DATA_FILE_PATH'))
        stations = load_stations(get_stations(df))
        load_railway_lines(df, stations)
        session.commit()
    except BaseException as e:
        print('An exception occurred: {}'.format(e))
    finally:
        session.close()


if __name__ == "__main__":
    main()
