"""Hydraulic model calibration related function module."""
import datetime as dt
from typing import Any, Union
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statista.metrics as pf
from geopandas import GeoDataFrame
from loguru import logger
from matplotlib.figure import Figure
from pandas._libs.tslibs.timestamps import Timestamp
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from serapeum_utils.utils import class_attr_initialize

from serapis.serapis_warnings import SilenceShapelyWarning
from serapis.river import River

data_fn = lambda x: dt.datetime.strptime(x, "%Y-%m-%d")

SilenceShapelyWarning()


class Calibration(River):
    """Hydraulic model Calibration.

    Hydraulic model calibration class
    """

    hm_gauges: DataFrame
    rrm_gauges: DataFrame

    calibration_attributes = dict(
        q_hm=None,
        wl_hm=None,
        q_rrm=None,
        q_rrm2=None,
        rrm_gauges=None,
        hm_gauges=None,
        q_gauges=None,
        wl_gauges=None,
        calibration_q=None,
        calibration_wl=None,
        annual_max_obs_q=None,
        annual_max_obs_wl=None,
        annual_max_rrm=None,
        annual_max_hm_q=None,
        annual_max_hm_wl=None,
        annual_max_dates=None,
        metrics_hm_vs_rrm=None,
        metrics_rrm_vs_obs=None,
        metrics_hm_wl_vs_obs=None,
        metrics_hm_q_vs_obs=None,
        wl_gauges_list=None,
        q_gauges_list=None,
    )

    @class_attr_initialize(calibration_attributes)
    def __init__(
        self,
        name: str,
        version: int = 3,
        start: Union[str, dt.datetime] = "1950-1-1",
        days: int = 36890,
        fmt: str = "%Y-%m-%d",
        rrm_start: str = None,
        rrm_days: int = 36890,
        no_data_value: int = -9,
        gauge_id_col: Any = "oid",
    ):
        """HMCalibration.

            To instantiate the calibration object, you have to provide the following arguments.

        Parameters
        ----------
        name : [str]
            name of the catchment.
        version: [integer], optional
            The version of the model. The default is 3.
        start: [str], optional
            starting date. The default is "1950-1-1".
        days: [integer], optional
            length of the simulation. The default is 36890. (default number of days is equivalent to 100 years)
        fmt: [str]
            format of the given dates. The default is "%Y-%m-%d"
        rrm_start: [str], optional
            the start date of the rainfall-runoff data. The default is "1950-1-1".
        rrm_days: [integer], optional
            the length of the data of the rainfall-runoff data in days. The default is 36890.
        gauge_id_col: [Any]
            the name of the column where the used id of the gauges is stored. Default is 'oid'

        Returns
        -------
        None.
        """
        # super().__init__()
        self.name = name
        self.version = version
        if isinstance(start, str):
            self.start = dt.datetime.strptime(start, fmt)
        self.end = self.start + dt.timedelta(days=days)
        self.days = days
        self.no_data_value = no_data_value
        self.gauge_id_col = gauge_id_col

        ref_ind = pd.date_range(self.start, self.end, freq="D")
        self.reference_index = pd.DataFrame(index=list(range(1, days + 1)))
        self.reference_index["date"] = ref_ind[:-1]

        if rrm_start is None:
            self.rrm_start = self.start
        else:
            try:
                self.rrm_start = dt.datetime.strptime(rrm_start, fmt)
            except ValueError:
                logger.debug(
                    f"please check the fmt ({fmt}) you entered as it is different from the rrm_start data ({rrm_start})"
                )
                return

        self.rrm_end = self.rrm_start + dt.timedelta(days=rrm_days)
        ref_ind = pd.date_range(self.rrm_start, self.rrm_end, freq="D")
        self.rrm_reference_index = pd.DataFrame(index=list(range(1, rrm_days + 1)))
        self.rrm_reference_index["date"] = ref_ind[:-1]

    def read_gauges_table(self, path: str):
        """ReadGaugesTable.

        readGaugesTable reads the table of the gauges

        Parameters
        ----------
        path : [String]
            the path to the text file of the gauges' table. the file can be geojson or a csv file.
        >>> "gauges.geojson"
        >>> {
        >>> "type": "FeatureCollection", "crs":
        >>>                                 { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3035" } },
        >>> "features": [
        >>> { "type": "Feature", "properties": { "gid": 149, "name": "station 1", "oid": 23800100, "river": "Nile",
        >>>     "id": 1, "xsid": 16100, "datum(m)": 252.36, "discharge": 1, "waterlevel": 1 },
        >>>     "geometry": { "type": "Point", "coordinates": [ 4278240.4259, 2843958.863 ] } },
        >>> { "type": "Feature", "properties": { "gid": 106, "name": "station 2", "oid": 23800500, "river": "Nile",
        >>>     "id": 2, "xsid": 16269, "datum(m)": 159.37, "discharge": 1, "waterlevel": 1 },
        >>>     "geometry": { "type": "Point", "coordinates": [ 4259614.333, 2884750.556 ] } },
        >>> { "type": "Feature", "properties": { "gid": 158, "name": "station 3", "oid": 23800690, "river": "Nile",
        >>>     "id": 4, "xsid": 16581, "datum(m)": 119.71, "discharge": 1, "waterlevel": 1},
        >>>     "geometry": { "type": "Point", "coordinates": [ 4248756.490, 2924872.503 ] } },
        >>> ]
        >>> }

        Returns
        -------
        GaugesTable: [dataframe attribute]
            the table will be read in a dataframe attribute

        Examples
        --------
        >>> import serapis.hm.calibration as rc
        >>> Calib = rc.Calibration("Hydraulic model", gauge_id_col="id")
        >>> Calib.read_gauges_table("path/to/gauges.geojson")
        >>> Calib.hm_gauges
        >>>     gid  ...                         geometry
        >>> 0   149  ...  POINT (4278240.426 2843958.864)
        >>> 1   106  ...  POINT (4259614.334 2884750.556)
        """
        if not Path(path).exists():
            raise FileNotFoundError(
                f"The gauges file you have entered: {path} does not exist"
            )

        try:
            self.hm_gauges = gpd.read_file(path, driver="GeoJSON")
        except Exception as e:
            logger.warning(
                f"the {path} could not be opened with geopandas and will be opened with pandas instead"
            )
            self.hm_gauges = pd.read_csv(path)

        # sort the gauges' table based on the reach
        self.hm_gauges.sort_values(by="id", inplace=True, ignore_index=True)

    def get_gauges(self, reach_id: int, gauge_id: int = 0) -> DataFrame:
        """get_gauges.

            get the id of the station for a given river reach.

        Parameters
        ----------
        reach_id: [int]
            the river reach id.
        gauge_id: [int]
            gauge id. Default is 0.

        Returns
        -------
        id: [list/int]
            if the river reach contains more than one gauges the function
            returns a list of ids, otherwise it returns the id.
        gauge name: [str]
            name of the gauge
        gauge xs: [int]
            the nearest cross section to the gauge
        """
        gauges = self.hm_gauges.loc[self.hm_gauges["id"] == reach_id, :].reset_index()
        if len(gauges) == 0:
            raise KeyError(
                "The given river reach does not have gauges in the gauge table"
            )
        elif len(gauges) > 1:
            f = gauges.loc[gauge_id, :].to_frame()
            gauge = pd.DataFrame(index=[0], columns=f.index.to_list())
            gauge.loc[0, :] = f.loc[f.index.to_list(), gauge_id].values.tolist()
            return gauge
        else:
            return gauges
        # stationname = gauges.loc[:, column].values.tolist()
        # gaugename = str(gauges.loc[gauge_id, 'name'])
        # gaugexs = gauges.loc[gauge_id, 'xsid']
        # reach_xs = str(reach_id) + "_" + str(gaugexs)

        # stationname, gaugename, gaugexs

    def read_observed_wl(
        self,
        path: str,
        start: Union[str, dt.datetime],
        end: Union[str, dt.datetime],
        no_data_value: Union[int, float],
        fmt="%Y-%m-%d",
        file_extension: str = ".txt",
        gauge_date_format="%Y-%m-%d",
    ):
        """ReadObservedWL.

        read the water level data of the gauges.

        Parameters
        ----------
        path: [str]
              path to the folder containing the text files of the water level gauges.
        start: [datetime object/str]
            the starting date of the water level time series.
        end: [datetime object/str]
            the end date of the water level time series.
        no_data_value : [integer/float]
            value used to fill the missing values.
        fmt: [str]
            format of the given dates. The default is "%Y-%m-%d"
        file_extension: [str]
            extension of the files. Default is ".txt"
        gauge_date_format: [str]
            format of the date in the first column in the gauges' files. Default is "%Y-%m-%d".

        Returns
        -------
        wl_gauges: [dataframe attribute].
            dataframe containing the data of the water level gauges and
            the index as the time series from the StartDate till the end
            and the gaps filled with the NoValue
        hm_gauges:[dataframe attribute].
            in the hm_gauges dataframe, two new columns are inserted
            ["WLstart", "WLend"] for the start and end date of the time
            series.
        """
        if isinstance(start, str):
            start = dt.datetime.strptime(start, fmt)
        if isinstance(end, str):
            end = dt.datetime.strptime(end, fmt)

        columns = self.hm_gauges[self.gauge_id_col].tolist()

        ind = pd.date_range(start, end)
        gauges = pd.DataFrame(index=ind)
        gauges.loc[:, 0] = ind
        logger.debug("Reading water level gauges data")
        for i in range(len(columns)):
            if self.hm_gauges.loc[i, "waterlevel"] == 1:
                name = self.hm_gauges.loc[i, self.gauge_id_col]
                try:
                    f = pd.read_csv(
                        path + str(int(name)) + file_extension, delimiter=",", header=0
                    )
                    f.columns = [0, 1]
                    f[0] = f[0].map(
                        lambda x: dt.datetime.strptime(x, gauge_date_format)
                    )
                    # sort by date as some values are missed up
                    f.sort_values(by=[0], ascending=True, inplace=True)
                    # filter to the range we want
                    f = f.loc[f[0] >= ind[0], :]
                    f = f.loc[f[0] <= ind[-1], :]
                    # reindex
                    f.index = list(range(len(f)))
                    # add datum and convert to meter
                    f.loc[f[1] != no_data_value, 1] = (
                        f.loc[f[1] != no_data_value, 1] / 100
                    ) + self.hm_gauges.loc[i, "datum(m)"]
                    f = f.rename(columns={1: columns[i]})

                    # use merge as there are some gaps in the middle
                    gauges = gauges.merge(f, on=0, how="left", sort=False)

                    logger.debug(f"{i} - {path}{name}{file_extension} is read")

                except FileNotFoundError:
                    logger.debug(f"{i} - {path}{name}{file_extension} has a problem")
                    return

        gauges.replace(to_replace=np.nan, value=no_data_value, inplace=True)
        gauges.index = ind
        del gauges[0]
        self.wl_gauges = gauges

        self.hm_gauges["WLstart"] = 0
        self.hm_gauges["WLend"] = 0
        for i in range(len(columns)):
            if self.hm_gauges.loc[i, "waterlevel"] == 1:
                st1 = self.wl_gauges[columns[i]][
                    self.wl_gauges[columns[i]] != no_data_value
                ].index[0]
                end1 = self.wl_gauges[columns[i]][
                    self.wl_gauges[columns[i]] != no_data_value
                ].index[-1]
                self.hm_gauges.loc[i, "WLstart"] = st1
                self.hm_gauges.loc[i, "WLend"] = end1

    # @staticmethod
    # def readfile(path,date_format):
    #
    #     ind = pd.date_range(start, end)
    #     Gauges = pd.DataFrame(index=ind)
    #     Gauges.loc[:, 0] = ind
    #     logger.debug("Reading discharge gauges data")
    #     for i in range(len(self.hm_gauges)):
    #         if self.hm_gauges.loc[i, "discharge"] == 1:
    #             name = self.hm_gauges.loc[i, column]
    #             try:
    #                 f = pd.read_csv(path, delimiter=",", header=0)
    #                 logger.debug(f"{i} - {path} is read")
    #
    #             except FileNotFoundError:
    #                 logger.debug(f"{i} - {path} has a problem")
    #                 return
    #             f.columns = [0, 1]
    #             f[0] = f[0].map(lambda x: dt.datetime.strptime(x, date_format))
    #             # sort by date as some values are missed up
    #             f.sort_values(by=[0], ascending=True, inplace=True)
    #             # filter to the range we want
    #             f = f.loc[f[0] >= ind[0], :]
    #             f = f.loc[f[0] <= ind[-1], :]
    #             # reindex
    #             f.index = list(range(len(f)))
    #             f = f.rename(columns={1: name})
    #
    #             # use merge as there are some gaps in the middle
    #             Gauges = Gauges.merge(f, on=0, how="left", sort=False)
    #
    #     Gauges.replace(to_replace=np.nan, value=no_data_value, inplace=True)
    #     Gauges.index = ind
    #     del Gauges[0]

    def read_observed_q(
        self,
        path: str,
        start: Union[str, dt.datetime],
        end: Union[str, dt.datetime],
        no_data_value: Union[int, float],
        fmt: str = "%Y-%m-%d",
        file_extension: str = ".txt",
        gauge_date_format="%Y-%m-%d",
    ):
        """readObservedQ.

            ReadObservedQ method reads discharge data and, stores it in a dataframe
            attribute "q_gauges"

        Parameters
        ----------
        path : [String]
            path to the folder where files for the gauges exist.
        start: [datetime object]
            starting date of the time series.
        end: [datetime object]
            ending date of the time series.
        no_data_value: [numeric]
            value stored in gaps.
        fmt : [str]
            format of the given dates. The default is "%Y-%m-%d"
        file_extension: [str]
            extension of the files. Default is ".txt"
        gauge_date_format: [str]
            format of the date in the first column in the gauges' files. Default is "%Y-%m-%d".

        Returns
        -------
        q_gauges:[dataframe attribute]
            dataframe containing the hydrograph of each gauge under a column
             by the name of gauge.
        hm_gauges:[dataframe attribute]
            in the hm_gauges dataframe two new columns are inserted
            ["Qstart", "Qend"] containing the start and end date of the
            discharge time series.
        """
        if isinstance(start, str):
            start = dt.datetime.strptime(start, fmt)
        if isinstance(end, str):
            end = dt.datetime.strptime(end, fmt)

        ind = pd.date_range(start, end)
        gauges = pd.DataFrame(index=ind)
        gauges.loc[:, 0] = ind
        logger.debug("Reading discharge gauges data")
        for i in range(len(self.hm_gauges)):
            if self.hm_gauges.loc[i, "discharge"] == 1:
                name = self.hm_gauges.loc[i, self.gauge_id_col]
                try:
                    f = pd.read_csv(
                        path + str(int(name)) + file_extension, delimiter=",", header=0
                    )
                    logger.info(f"{i} - {path}{name}{file_extension} is read")

                except FileNotFoundError:
                    logger.debug(f"{i} - {path}{name}{file_extension} has a problem")
                    continue
                f.columns = [0, 1]
                f[0] = f[0].map(lambda x: dt.datetime.strptime(x, gauge_date_format))
                # sort by date as some values are missed up
                f.sort_values(by=[0], ascending=True, inplace=True)
                # filter to the range we want
                f = f.loc[f[0] >= ind[0], :]
                f = f.loc[f[0] <= ind[-1], :]
                # reindex
                f.index = list(range(len(f)))
                f = f.rename(columns={1: name})

                # use merge as there are some gaps in the middle
                gauges = gauges.merge(f, on=0, how="left", sort=False)

        gauges.replace(to_replace=np.nan, value=no_data_value, inplace=True)
        gauges.index = ind
        del gauges[0]
        # try:
        #     q_gauges.loc[:, int(name)] = np.loadtxt(
        #         path + str(int(name)) + file_extension
        #     )  # ,skiprows = 0
        #
        #     logger.debug(f"{i} - {path}{name}{file_extension} is read")
        # except FileNotFoundError:
        #     logger.debug(f"{i} - {path}{name}{file_extension} has a problem")
        #     return
        # name = self.hm_gauges.loc[i, column]

        self.q_gauges = gauges
        self.hm_gauges["Qstart"] = 0
        self.hm_gauges["Qend"] = 0

        for i in range(len(self.hm_gauges)):
            if self.hm_gauges.loc[i, "discharge"] == 1:
                ii = self.hm_gauges.loc[i, self.gauge_id_col]
                st1 = self.q_gauges[ii][self.q_gauges[ii] != no_data_value].index[0]
                end1 = self.q_gauges[ii][self.q_gauges[ii] != no_data_value].index[-1]
                self.hm_gauges.loc[i, "Qstart"] = st1
                self.hm_gauges.loc[i, "Qend"] = end1

    def read_rrm(
        self,
        path: str,
        from_day: Union[str, int] = "",
        to_day: Union[str, int] = "",
        fmt: str = "%Y-%m-%d",
        location: int = 1,
        path2: str = "",
    ):
        """ReadRRM.

            ReadRRM method reads the discharge results of the rainfall runoff
            model and stores it in a dataframe attribute "q_rrm"

        Parameters
        ----------
        path : [String]
            path to the folder where files for the gauges exist.
        from_day: [datetime object]
            starting date of the time series.
        to_day: [datetime object]
            ending date of the time series.
        fmt: [str]
            format of the given dates. The default is "%Y-%m-%d"
        location: [int]
            the RRM hydrographs for a 2nd location
        path2: [str]
            directory where the RRM hydrographs for the 2nd location are saved

        Returns
        -------
        q_rrm: [dataframe]
            rainfall-runoff discharge time series stored in a dataframe with
            the columns as the gauges id and the index are the time.
        rrm_gauges: [list]
            list og gauges id
        """
        gauges = self.hm_gauges.loc[
            self.hm_gauges["discharge"] == 1, self.gauge_id_col
        ].tolist()

        self.q_rrm = pd.DataFrame()
        if location == 2:
            # create a dataframe for the 2nd time series of the rainfall runoff
            # model at the second location
            self.rrm_discharge_2 = pd.DataFrame()

        self.rrm_gauges = []
        if path == "":
            path = self.rrmpath

        if location == 2:
            if path2 == "":
                raise ValueError(
                    "path2 argument has to be given for the location of the 2nd rainfall run-off time series"
                )

        if location == 1:
            for i in range(len(gauges)):
                station_id = gauges[i]
                try:
                    self.q_rrm[station_id] = self._read_rrm_results(
                        self.version,
                        self.rrm_reference_index,
                        path,
                        station_id,
                        from_day,
                        to_day,
                        date_format=fmt,
                    )[station_id].tolist()
                    logger.info(f"{i} - {path}{station_id}.txt is read")
                    self.rrm_gauges.append(station_id)
                except FileNotFoundError:
                    logger.info(
                        f"{i} - {path}{station_id}.txt does not exist or have a problem"
                    )
        else:
            for i in range(len(gauges)):
                station_id = gauges[i]
                try:
                    self.q_rrm[station_id] = self._read_rrm_results(
                        self.version,
                        self.rrm_reference_index,
                        path,
                        station_id,
                        from_day,
                        to_day,
                        date_format=fmt,
                    )[station_id].tolist()
                    self.rrm_discharge_2[station_id] = self._read_rrm_results(
                        self.version,
                        self.rrm_reference_index,
                        path2,
                        station_id,
                        from_day,
                        to_day,
                        date_format=fmt,
                    )[station_id].tolist()
                    logger.info(f"{i} - {path}{station_id}.txt is read")
                    self.rrm_gauges.append(station_id)
                except FileNotFoundError:
                    logger.info(
                        f"{i} - {path}{station_id}.txt does not exist or have a problem"
                    )
        # logger.debug("RRM time series for the gauge " + str(station_id) + " is read")

        if from_day == "":
            from_day = 1
        if to_day == "":
            to_day = len(self.q_rrm[self.q_rrm.columns[0]])

        start = self.reference_index.loc[from_day, "date"]
        end = self.reference_index.loc[to_day, "date"]

        if location == 1:
            self.q_rrm.index = pd.date_range(start, end, freq="D")
        else:
            self.q_rrm.index = pd.date_range(start, end, freq="D")
            self.rrm_discharge_2.index = pd.date_range(start, end, freq="D")

    def read_hm_discharge(
        self,
        path: str,
        from_day: Union[str, int] = "",
        to_day: Union[str, int] = "",
        no_data_value: Union[int, float] = -9,
        add_hq2: bool = False,
        shift: bool = False,
        shift_steps: int = 0,
        fmt: str = "%Y-%m-%d",
    ):
        """ReadHMQ.

        Read Hydraulic model discharge time series.

        Parameters
        ----------
        path: [String]
            path to the folder where files for the gauges exist.
        from_day: [datetime object/str]
            starting date of the time series.
        to_day: [integer]
            length of the simulation (how many days after the start date).
        no_data_value: [numeric value]
            the value used to fill the gaps in the time series or to fill the
            days that is not simulated (discharge is less than a threshold).
        add_hq2: [bool]
            for version 1 the HQ2 can be added to the simulated hydrograph to
            compare it with the gauge data. default is False.
        shift: [bool]
            boolean value to decide whither to shift the time series or not.
            default is False.
        shift_steps: [integer]
            number of time steps to shift the time series could be negative integer to shift the time series
            backward. default is 0.
        fmt: [str]
            format of the given dates. The default is "%Y-%m-%d"

        Returns
        -------
        q_hm: [dataframe attribute]
            dataframe containing the simulated hydrograph for each river reach in the catchment.
        """
        if add_hq2 and self.version == 1:
            msg = "please read the traceall file using the RiverNetwork method"
            assert hasattr(self, "river_network"), msg
            msg = "please read the HQ file first using ReturnPeriod method"
            assert hasattr(self, "RP"), msg

        gauges = self.hm_gauges.loc[
            self.hm_gauges["discharge"] == 1, self.gauge_id_col
        ].tolist()
        self.discharge_gauges_list = gauges
        self.q_hm = pd.DataFrame()

        # for RIM1.0 don't fill with -9 as the empty days will be filled
        # with 0 so to get the event days we have to filter 0 and -9
        # if self.version == 1:
        #     q_hm.loc[:, :] = 0
        # else:
        #     q_hm.loc[:, :] = no_data_value

        # fill non modelled time steps with zeros
        for i in range(len(gauges)):
            node_id = gauges[i]
            self.q_hm[node_id] = self._read_rrm_results(
                self.version,
                self.reference_index,
                path,
                node_id,
                from_day=None,
                to_day=None,
                date_format=fmt,
            )[node_id].tolist()
            logger.debug(f"{i} - {path}{node_id}.txt is read")

            if add_hq2 and self.version == 1:
                upstream_node = self.river_network.loc[
                    np.where(
                        self.river_network["id"]
                        == self.hm_gauges.loc[i, self.gauge_id_col]
                    )[0][0],
                    "us",
                ]

                cut_value = self.RP.loc[
                    np.where(self.RP["node"] == upstream_node)[0][0], "HQ2"
                ]
                print(cut_value)

            # for j in range(len(f1)):
            #     # if the index exist in the original list
            #     if f1[j] in f[:, 0]:
            #         # put the coresponding value in f2
            #         f2.append(f[np.where(f[:, 0] == f1[j])[0][0], 1])
            #     else:
            #         # if it does not exist put zero
            #         if add_hq2 and self.version == 1:
            #             f2.append(cut_value)
            #         else:
            #             f2.append(0)

            # if shift:
            #     f2[shift_steps:-1] = f2[0 : -(shift_steps + 1)]

            # q_hm.loc[ind[f1[0] - 1] : ind[f1[-1] - 1], q_hm.columns[i]] = f2
        if from_day == "":
            from_day = 1
        if to_day == "":
            to_day = len(self.q_hm[self.q_hm.columns[0]])

        start = self.reference_index.loc[from_day, "date"]
        end = self.reference_index.loc[to_day, "date"]

        self.q_hm.index = pd.date_range(start, end, freq="D")

    def read_hm_water_level(
        self,
        path: str,
        from_day: Union[str, int] = "",
        to_day: Union[str, int] = "",
        no_data_value: Union[int, float] = -9,
        shift=False,
        shift_steps=0,
        column: str = "oid",
        fmt: str = "%Y-%m-%d",
    ):
        """ReadRIMWL.

        Parameters
        ----------
        path: [String]
            path to the folder where files for the gauges exist.
        from_day: [datetime object/str]
            starting date of the time series.
        to_day: [integer]
            end date of the time series.
        no_data_value: [numeric value]
            the value used to fill the gaps in the time series or to fill the
            days that is not simulated (discharge is less than a threshold).
        shift: [bool]
            boolean value to decide whither to shift the time series or not.
            default is False.
        shift_steps: [integer]
            number of time steps to shift the time series could be negative
            integer to shift the time series backward. default is 0.
        column: [string]
            name of the column that contains the gauges' file name. default is 'oid'.
        fmt: [str]
            format of the given dates. The default is "%Y-%m-%d".

        Returns
        -------
        wl_hm: [dataframe attribute]
            dataframe containing the simulated water level hydrograph for
            each river reach in the catchment.
        """
        gauges = self.hm_gauges.loc[
            self.hm_gauges["waterlevel"] == 1, self.gauge_id_col
        ].tolist()
        self.wl_gauges_list = gauges

        self.wl_hm = pd.DataFrame()
        for i in range(len(gauges)):
            node_id = gauges[i]
            self.wl_hm[node_id] = self._read_rrm_results(
                self.version,
                self.reference_index,
                path,
                node_id,
                from_day="",
                to_day="",
                date_format=fmt,
            )[node_id].tolist()
            logger.debug(f"{i} - {path}{node_id}.txt is read")
        # for i in range(len(wl_hm.columns)):
        #     f = np.loadtxt(path + str(int(wl_hm.columns[i])) + ".txt", delimiter=",")
        #
        #     f1 = list(range(int(f[0, 0]), int(f[-1, 0]) + 1))
        #     f2 = list()
        #     for j in range(len(f1)):
        #         # if the index exist in the original list
        #         if f1[j] in f[:, 0]:
        #             # put the coresponding value in f2
        #             f2.append(f[np.where(f[:, 0] == f1[j])[0][0], 1])
        #         else:
        #             # if it does not exist put zero
        #             f2.append(0)
        #
        #     if shift:
        #         f2[shift_steps:-1] = f2[0 : -(shift_steps + 1)]

        # wl_hm.loc[ind[f1[0] - 1] : ind[f1[-1] - 1], wl_hm.columns[i]] = f2
        if from_day == "":
            from_day = 1
        if to_day == "":
            to_day = len(self.wl_hm[self.wl_hm.columns[0]])

        start = self.reference_index.loc[from_day, "date"]
        end = self.reference_index.loc[to_day, "date"]

        self.wl_hm.index = pd.date_range(start, end, freq="D")

    def read_calibration_result(self, reach_id: int, path: str = ""):
        """read_calibration_result.

            read_calibration_result method reads the 1D results and fills the missing days in the middle.

        Parameters
        ----------
        reach_id: [integer]
            ID of the sub-basin you want to read its data.
        path: [String], optional
            Path to read the results from. The default is ''.

        Returns
        -------
        calibration_q : [dataframe]
            the discharge time series of the calibrated gauges.
        calibration_wl : [dataframe]
            the water level time series of the calibrated gauges.
        """
        hasattr(self, "q_gauges"), "Please read the discharge gauges first"
        hasattr(self, "WlGauges"), "Please read the water level gauges first"

        if not hasattr(self, "calibration_q"):
            ind_d = pd.date_range(self.start, self.end, freq="D")[:-1]
            self.CalibrationQ = pd.DataFrame(index=ind_d)
        if not hasattr(self, "calibration_wl"):
            ind_d = pd.date_range(self.start, self.end, freq="D")[:-1]
            self.CalibrationWL = pd.DataFrame(index=ind_d)

        ind = pd.date_range(self.start, self.end, freq="H")[:-1]
        q = pd.read_csv(path + str(reach_id) + "_q.txt", header=None, delimiter=r"\s+")
        wl = pd.read_csv(
            path + str(reach_id) + "_wl.txt", header=None, delimiter=r"\s+"
        )

        q.index = ind
        wl.index = ind

        self.CalibrationQ[reach_id] = q[1].resample("D").mean()
        self.CalibrationWL[reach_id] = wl[1].resample("D").mean()

    def get_annual_max(
        self, option=1, corresponding_to=dict(MaxObserved=" ", TimeWindow=0)
    ):
        """get_annual_max.

            get_annual_max method gets the max annual time series out of time series of any temporal resolution.
            The code assumes that the hydrological year is 1-Nov/31-Oct (Petrow and Merz, 2009, JoH).

        Parameters
        ----------
        option: [integer], optional
            - 1 for the historical observed Discharge data.
            - 2 for the historical observed water level data.
            - 3 for the rainfall-runoff data.
            - 4 for the hm discharge result.
            - 5 for the hm water level result.
            The default is 1.

        corresponding_to: [Dict], optional
            - if you want to extract the max annual values from the observed discharge time series (
            corresponding_to=dict(MaxObserved = "Q") and then extract the values of the same dates in the simulated time
            series. The same for observed water level time series (corresponding_to=dict(MaxObserved = "WL").
            or if you just want to extract the max annual values from each time series (corresponding_to=dict(
            MaxObserved = " "). The default is " ".

            - if you want to extract some values before and after the corresponding date and then take the max value
            of all extracted values specify the number of days using the keyword Window corresponding_to=dict(
            TimeWindow = 1)

        Returns
        -------
        annual_max_obs_q: [dataframe attribute]
            when using Option=1
        annual_max_obs_wl: [dataframe attribute]
            when using option = 2
        annual_max_rrm: [dataframe attribute]
            when using option = 3
        AnnualMaxRIMQ: [dataframe attribute]
            when using option = 4
        annual_max_hm_wl: [dataframe attribute]
            when using option = 5
        annual_max_dates : [dataframe attribute]
        """
        if option == 1:
            if not isinstance(self.q_gauges, DataFrame):
                raise ValueError(
                    "please read the observed Discharge data first with the"
                    "ReadObservedQ method "
                )
            columns = self.q_gauges.columns.tolist()
        elif option == 2:
            if not isinstance(self.wl_gauges, DataFrame):
                raise ValueError(
                    "please read the observed Water level data first with the "
                    "ReadObservedWL method"
                )
            columns = self.wl_gauges.columns.tolist()
        elif option == 3:
            if not isinstance(self.q_rrm, DataFrame):
                raise ValueError(
                    "please read the Rainfall-runoff data first with the "
                    "ReadRRM method"
                )
            columns = self.q_rrm.columns.tolist()
        elif option == 4:
            if not isinstance(self.q_hm, DataFrame):
                raise ValueError(
                    "please read the RIM results first with the ReadRIMQ method "
                )
            columns = self.q_hm.columns.tolist()
        else:
            if not isinstance(self.wl_hm, DataFrame):
                raise ValueError(
                    "please read the RIM results first with the ReadRIMWL method"
                )
            columns = self.wl_hm.columns.tolist()

        if corresponding_to["MaxObserved"] == "WL":
            if not isinstance(self.wl_gauges, DataFrame):
                raise ValueError(
                    "please read the observed Water level data first with the "
                    "ReadObservedWL method"
                )

            start_date = self.wl_gauges.index[0]
            annual_max = (
                self.wl_gauges.loc[:, self.wl_gauges.columns[0]].resample("A-OCT").max()
            )
            self.AnnualMaxDates = pd.DataFrame(
                index=annual_max.index, columns=self.wl_gauges.columns
            )

            # get the dates when the max value happens every year
            for i in range(len(self.wl_gauges.columns)):
                sub = self.wl_gauges.columns[i]
                for j in range(len(annual_max)):
                    if j == 0:
                        f = self.wl_gauges.loc[start_date : annual_max.index[j], sub]
                        self.AnnualMaxDates.loc[annual_max.index[j], sub] = f.index[
                            f.argmax()
                        ]
                    else:
                        f = self.wl_gauges.loc[
                            annual_max.index[j - 1] : annual_max.index[j], sub
                        ]
                        self.AnnualMaxDates.loc[annual_max.index[j], sub] = f.index[
                            f.argmax()
                        ]

            # extract the values at the dates of the previous max value
            annual_max = pd.DataFrame(index=self.AnnualMaxDates.index, columns=columns)

            # Extract time series
            for i in range(len(columns)):
                sub = columns[i]
                qts = list()

                if option == 1:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.q_gauges.loc[start:end, sub].max())
                elif option == 2:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=1)
                        end = date + dt.timedelta(days=1)
                        qts.append(self.wl_gauges.loc[start:end, sub].max())
                elif option == 3:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.q_rrm.loc[start:end, sub].max())
                elif option == 4:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.q_hm.loc[start:end, sub].max())
                else:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.wl_hm.loc[start:end, sub].max())

                annual_max.loc[:, sub] = qts

        elif corresponding_to["MaxObserved"] == "Q":
            if not isinstance(self.q_gauges, DataFrame):
                raise ValueError(
                    "please read the observed Discharge data first with the"
                    "ReadObservedQ method"
                )
            start_date = self.q_gauges.index[0]
            annual_max = (
                self.q_gauges.loc[:, self.q_gauges.columns[0]].resample("A-OCT").max()
            )
            self.AnnualMaxDates = pd.DataFrame(
                index=annual_max.index, columns=self.q_gauges.columns
            )

            # get the date when the max value happens every year
            for i in range(len(self.q_gauges.columns)):
                sub = self.q_gauges.columns[i]
                for j in range(len(annual_max)):
                    if j == 0:
                        f = self.q_gauges.loc[start_date : annual_max.index[j], sub]
                        self.AnnualMaxDates.loc[annual_max.index[j], sub] = f.index[
                            f.argmax()
                        ]
                    else:
                        f = self.q_gauges.loc[
                            annual_max.index[j - 1] : annual_max.index[j], sub
                        ]
                        self.AnnualMaxDates.loc[annual_max.index[j], sub] = f.index[
                            f.argmax()
                        ]

            # extract the values at the dates of the previous max value
            annual_max = pd.DataFrame(index=self.AnnualMaxDates.index, columns=columns)
            # Extract time series
            for i in range(len(columns)):
                sub = columns[i]
                qts = list()

                if option == 1:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.q_gauges.loc[start:end, sub].max())

                elif option == 2:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.wl_gauges.loc[start:end, sub].max())

                elif option == 3:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.q_rrm.loc[start:end, sub].max())

                elif option == 4:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.q_hm.loc[start:end, sub].max())
                else:
                    for j in range(len(self.AnnualMaxDates.loc[:, sub])):
                        ind = self.AnnualMaxDates.index[j]
                        date = self.AnnualMaxDates.loc[ind, sub]
                        start = date - dt.timedelta(days=corresponding_to["TimeWindow"])
                        end = date + dt.timedelta(days=corresponding_to["TimeWindow"])
                        qts.append(self.wl_hm.loc[start:end, sub].max())

                # resample to an annual time step.
                annual_max.loc[:, sub] = qts
        else:
            annual_max = pd.DataFrame(columns=columns)
            # Extract time series
            for i in range(len(columns)):
                sub = columns[i]
                if option == 1:
                    qts = self.q_gauges.loc[:, sub]
                elif option == 2:
                    qts = self.wl_gauges.loc[:, sub]
                elif option == 3:
                    qts = self.q_rrm.loc[:, sub]
                elif option == 4:
                    qts = self.q_hm.loc[:, sub]
                else:
                    qts = self.wl_hm.loc[:, sub]
                # resample to an annual time step.
                annual_max.loc[:, sub] = qts.resample("A-OCT").max().values

            annual_max.index = qts.resample("A-OCT").indices.keys()

        if option == 1:
            self.annual_max_obs_q = annual_max
        elif option == 2:
            self.annual_max_obs_wl = annual_max
        elif option == 3:
            self.annual_max_rrm = annual_max
        elif option == 4:
            self.annual_max_hm_q = annual_max
        else:
            self.annual_max_hm_wl = annual_max

    def calculate_profile(
        self,
        reach_id: int,
        bed_level_downstream: float,
        manning_coefficient: float,
        boundary_condition_slope: float,
    ):
        """CalculateProfile.

        CalculateProfile method takes the river reach ID and the calibration
        parameters (last downstream cross-section bed level and the manning
        coefficient) and calculates the new profiles.

        Parameters
        ----------
        reach_id: [Integer]
            cross-sections reach ID.
        bed_level_downstream: [Float]
            the bed level of the last cross-section in the reach.
        manning_coefficient: [float]
            the manning coefficient.
        boundary_condition_slope: [float]
            slope of the BC.

        Returns
        -------
        cross-section:[dataframe attribute]
            cross-section attribute will be updated with the newly calculated profile for the given reach
        slope:[dataframe attribute]
            slope attribute will be updated with the newly calculated average slope for the given reach.
        """
        levels = pd.DataFrame(columns=["id", "bedlevelUS", "bedlevelDS"])

        # change cross-section
        bed_level = self.cross_sections.loc[
            self.cross_sections["id"] == reach_id, "gl"
        ].values
        # get the bed_level of the last cross section in the reach
        # as a calibration parameter
        levels.loc[reach_id, "bedlevelDS"] = bed_level_downstream
        levels.loc[reach_id, "bedlevelUS"] = bed_level[0]

        no_distances = len(bed_level) - 1
        # AvgSlope = ((levels.loc[reach_id,'bedlevelUS'] -
        #      levels.loc[reach_id,'bedlevelDS'] )/ (500 * no_distances)) *-500
        # change in the bed level of the last XS
        average_delta = (
            levels.loc[reach_id, "bedlevelDS"] - bed_level[-1]
        ) / no_distances

        # calculate the new bed levels
        bed_level_new = np.zeros(len(bed_level))
        bed_level_new[len(bed_level) - 1] = levels.loc[reach_id, "bedlevelDS"]
        bed_level_new[0] = levels.loc[reach_id, "bedlevelUS"]

        for i in range(len(bed_level) - 1):
            # bed_level_new[i] = levels.loc[reach_id,'bedlevelDS'] + (len(bed_level) - i -1) * abs(AvgSlope)
            bed_level_new[i] = bed_level[i] + i * average_delta

        self.cross_sections.loc[
            self.cross_sections["id"] == reach_id, "gl"
        ] = bed_level_new
        # change manning
        self.cross_sections.loc[
            self.cross_sections["id"] == reach_id, "m"
        ] = manning_coefficient
        # change slope
        try:
            # self.slope.loc[self.slope['id']==reach_id, 'slope'] = AvgSlope
            self.slope.loc[
                self.slope["id"] == reach_id, "slope"
            ] = boundary_condition_slope
        except AttributeError:
            logger.debug(f"The Given river reach- {reach_id} does not have a slope")

    def get_reach(self, reach_id: int) -> DataFrame:
        """get_reach.

            cross-section data.

        Parameters
        ----------
        reach_id: [int]
            reach id

        Returns
        -------
        DataFrame
        """
        return (
            self.cross_sections.loc[self.cross_sections["id"] == reach_id, :]
            .copy()
            .reset_index()
        )

    def update_reach(self, reach: DataFrame):
        """update_reach.

            Update the cross-section of a given reach in the cross_sections attributes.

        Parameters
        ----------
        reach: [DataFrame]
            DataFrame of the reach cross sections

        Returns
        -------
        Updates the cross_sections DataFrame attribute.
        """
        # get the reach id
        reach_id: np.ndarray = reach.loc[:, "id"].unique()
        if len(reach_id) > 1:
            raise ValueError(
                f"The given DataFrame contains more than one river reach: {len(reach_id)}, the function "
                "can update one reach at a time."
            )
        reach_id = reach_id[0]
        g = self.cross_sections.loc[self.cross_sections["id"] == reach_id, :].index[0]
        # reset the index to the original index order
        reach.index = range(g, g + len(reach))
        # copy back the reach to the whole XS df
        self.cross_sections.loc[self.cross_sections["id"] == reach_id, :] = reach

    @staticmethod
    def _smooth(series: Series, window: int = 3):
        """Smooth data in a specific column in the given DataFrame.

        Parameters
        ----------
        series: [series]
            Pandas Series.
        window: [int]
            window length (length of averaged values)

        Returns
        -------
        Pandas Series
        """
        # calculate the average of three XS bed levels
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html
        smoothed = series.rolling(window=window, center=True).mean()
        # the bed level at the beginning and end of the segment
        smoothed[0] = series[0]
        smoothed[smoothed.index[-1]] = series[series.index[-1]]

        return smoothed

    def smooth_bed_level(self, reach_id: int, window: int = 3):
        """smooth_bed_level.

            smooth_bed_level method smooths the bed level of a given reach ID by calculating the moving average of
            three cross sections

        Parameters
        ----------
        reach_id : [Integer]
            reach ID.
        window: [int]
            window length (length of averaged values)

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "gl" column in the cross_sections attribute will be smoothed
        """
        if not hasattr(self, "cross_sections"):
            raise ValueError("Please read the cross-section first")

        reach = self.get_reach(reach_id)
        reach["glnew"] = self._smooth(reach["gl"], window=window)
        # calculate the difference in the bed level and take it from
        # the bankfull_depth depth
        reach.loc[:, "diff"] = reach.loc[:, "glnew"] - reach.loc[:, "gl"]
        reach.loc[:, "dbf"] = reach.loc[:, "dbf"] - reach.loc[:, "diff"]
        reach.loc[:, "gl"] = reach.loc[:, "glnew"]
        reach.drop(labels=["glnew", "diff"], axis=1, inplace=True)

        self.update_reach(reach)

    def smooth_dike_level(self, reach_id: int, window: int = 3):
        """smooth_dike_level.

            smooth_dike_level method smooths the bed level of a given reach ID by calculating the moving average of
            three cross sections.

        Parameters
        ----------
        reach_id : [Integer]
            reach ID.
        window: [int]
            window length (length of averaged values)

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "gl" column in the cross_sections attribute will be smoothed
        """
        if not hasattr(self, "cross_sections"):
            raise ValueError("Please read the cross-section first")

        reach = self.get_reach(reach_id)
        reach["zl"] = self._smooth(reach["zl"], window=window)
        reach["zr"] = self._smooth(reach["zr"], window=window)
        self.update_reach(reach)

    def smooth_bank_level(self, reach_id: int, window: int = 3):
        """smooth_bank_level.

        smooth_bank_level method smooths the bankfull depth for a given reach.

        Parameters
        ----------
        reach_id : [Integer]
            Reach ID.
        window: [int]
            window length (length of averaged values)

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "dbf" column in the cross_sections attribute will be smoothed
        """
        self.cross_sections.loc[:, "banklevel"] = (
            self.cross_sections.loc[:, "dbf"] + self.cross_sections.loc[:, "gl"]
        )

        reach = self.get_reach(reach_id)
        reach["banklevelnew"] = self._smooth(reach["banklevel"], window=window)

        reach.loc[:, "diff"] = reach.loc[:, "banklevelnew"] - reach.loc[:, "banklevel"]
        # add the difference to the bankfull_depth depth
        reach.loc[:, "dbf"] = reach.loc[:, "dbf"] + reach.loc[:, "diff"]

        reach.drop(labels=["banklevel"], axis=1, inplace=True)
        self.update_reach(reach)

    def smooth_floodplain_height(self, reach_id: int, window: int = 3):
        """smooth_floodplain_height.

        smooth_floodplain_height method smooths the Floodplain Height the point 5 and 6 in the cross-section for a
        given reach.

        Parameters
        ----------
        reach_id : [Integer]
            reach ID.
        window: [int]
            window length (length of averaged values)

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "hl" and "hr" column in the cross_sections attribute will be
            smoothed.
        """
        self.cross_sections.loc[:, "banklevel"] = (
            self.cross_sections.loc[:, "dbf"] + self.cross_sections.loc[:, "gl"]
        )
        self.cross_sections.loc[:, "fpl"] = (
            self.cross_sections.loc[:, "hl"] + self.cross_sections.loc[:, "banklevel"]
        )
        self.cross_sections.loc[:, "fpr"] = (
            self.cross_sections.loc[:, "hr"] + self.cross_sections.loc[:, "banklevel"]
        )

        reach = self.get_reach(reach_id)

        reach["fplnew"] = self._smooth(reach["fpl"], window=window)
        reach["fprnew"] = self._smooth(reach["fpr"], window=window)

        reach.loc[:, "diff0"] = reach.loc[:, "fplnew"] - reach.loc[:, "fpl"]
        reach.loc[:, "diff1"] = reach.loc[:, "fprnew"] - reach.loc[:, "fpr"]

        reach.loc[:, "hl"] = reach.loc[:, "hl"] + reach.loc[:, "diff0"]
        reach.loc[:, "hr"] = reach.loc[:, "hr"] + reach.loc[:, "diff1"]

        self.update_reach(reach)
        self.cross_sections.drop(
            labels=["banklevel", "fpr", "fpl"], axis=1, inplace=True
        )

    def smooth_bed_width(self, reach_id: int, window: int = 3):
        """smooth_bed_width.

            smooth_bed_width method smooths the bed width in the cross-section for a given reach.

        Parameters
        ----------
        reach_id : [Integer]
            reach ID.
        window: [int]
            window length (length of averaged values)

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "b" column in the cross_sections attribute will be smoothed
        """
        reach = self.get_reach(reach_id)
        reach["n"] = self._smooth(reach["b"], window=window)
        self.update_reach(reach)

    def downward_bed_level(self, reach_id: int, height: Union[int, float]):
        """downward_bed_level.

            downward_bed_level lowering the bed level by a certain height (5 cm).

        Parameters
        ----------
        reach_id : [Integer]
            reach ID.
        height : []
            down

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "b" column in the cross_sections attribute will be smoothed
        """
        reach = self.get_reach(reach_id)

        for j in range(1, len(reach)):
            if reach.loc[j - 1, "gl"] - reach.loc[j, "gl"] < height:
                reach.loc[j, "gl"] = reach.loc[j - 1, "gl"] - height

        self.update_reach(reach)

    def smooth_max_slope(self, reach_id: int, slope_percent_threshold: float = 1.5):
        """SmoothMaxSlope.

        SmoothMaxSlope method smooths the bed levels in the cross-section.
        for a given reach

        As now the slope is not very smoothed as it was when using the average slope everywhere, when the difference
        between two consecutive slopes is very high, the difference is reflected in the calculated discharge from
        both cross-sections

        Qout is very high, Qin is smaller compared to Qout, and from the continuity equation the amount of water that
        stays at the cross-section is very few water(Qin3-Qout3), less than the minimum depth

        then the minimum depth is assigned at the cross-section, applying the minimum depth in all time steps will
        make the delta A / delta t equal zero As a result, the integration of delta Q/delta x will give a constant
        discharge for all the downstream cross-section.

        To overcome this limitation, a manual check is performed during the calibration process by visualizing the
        hydrographs of the first and last cross-section in the sub-basin and the water surface profile to make sure
        that the algorithm does not give a constant discharge.

        Parameters
        ----------
        reach_id: [Integer]
            reach ID.
        slope_percent_threshold: [Float]
             the percentage of change in a slope between three successive cross-sections. The default is 1.5.

        Returns
        -------
        cross_sections: [dataframe attribute]
            the "gl" column in the cross_sections attribute will be smoothed
        """
        reach = self.get_reach(reach_id)
        # slope must be positive due to the smoothing
        slopes = [
            (reach.loc[k, "gl"] - reach.loc[k + 1, "gl"]) / 500
            for k in range(len(reach) - 1)
        ]
        # if percent is -ve means the second slope is steeper
        percent = [
            (slopes[k] - slopes[k + 1]) / slopes[k] for k in range(len(slopes) - 1)
        ]

        # at row 1 in the percent list is the difference between row 1 and row 2
        # in slopes list and slope in row 2 is the steep slope,
        # slope at row 2 is the difference
        # between gl in row 2 and row 3 in the reach dataframe, and gl row
        # 3 is very, and we want to elevate it to reduce the slope
        for j in range(len(percent)):
            if percent[j] < 0 and abs(percent[j]) >= slope_percent_threshold:
                logger.debug(j)
                # get the calculated slope based on the slope percent threshold
                slopes[j + 1] = slopes[j] - (-slope_percent_threshold * slopes[j])
                reach.loc[j + 2, "gl"] = reach.loc[j + 1, "gl"] - slopes[j + 1] * 500
                # recalculate all the slopes again
                slopes = [
                    (reach.loc[k, "gl"] - reach.loc[k + 1, "gl"]) / 500
                    for k in range(len(reach) - 1)
                ]
                percent = [
                    (slopes[k] - slopes[k + 1]) / slopes[k]
                    for k in range(len(slopes) - 1)
                ]

        self.update_reach(reach)

    def check_floodplain(self):
        """check_floodplain.

            check_floodplain method checks if the dike levels are higher than the floodplain height (point 5 and 6
            has to be lower than point 7 and 8 in the cross-sections)

        Returns
        -------
        cross-section: [dataframe attribute]
            the "zl" and "zr" column in the "cross_sections" attribute will be updated.
        """
        msg = """please read the cross-section first or copy it to the Calibration object"""
        assert hasattr(self, "cross_sections"), "{0}".format(msg)
        for i in range(len(self.cross_sections)):
            bank_level = (
                self.cross_sections.loc[i, "gl"] + self.cross_sections.loc[i, "dbf"]
            )

            if (
                bank_level + self.cross_sections.loc[i, "hl"]
                > self.cross_sections.loc[i, "zl"]
            ):
                self.cross_sections.loc[i, "zl"] = (
                    bank_level + self.cross_sections.loc[i, "hl"] + 0.5
                )

            if (
                bank_level + self.cross_sections.loc[i, "hr"]
                > self.cross_sections.loc[i, "zr"]
            ):
                self.cross_sections.loc[i, "zr"] = (
                    bank_level + self.cross_sections.loc[i, "hr"] + 0.5
                )

    @staticmethod
    def metrics(
        df1: DataFrame,
        df2: DataFrame,
        gauges: list,
        no_data_value: int,
        start: str = "",
        end: str = "",
        shift: int = 0,
        fmt: str = "%Y-%m-%d",
    ) -> DataFrame:
        """Calculate performance metrics.

        Parameters
        ----------
        df1: [DataFrame]
            first dataframe, with columns as the gauges id and rows as the time series
        df2: [DataFrame]
            second dataframe, with columns as the gauges id and rows as the time series
        gauges: [list]
            list of gauges ids
        no_data_value:
            the value used to fill the missing values
        start:
            start date
        end:
            end date
        shift:
            shift in the days
        fmt:
            date format

        Returns
        -------
        GeoDataFrame:
            with the following columns ["start", "end", "rmse", "KGE", "WB", "NSE", "NSEModified"]
        """
        metrics = gpd.GeoDataFrame(
            index=gauges,
            columns=["start", "end", "rmse", "KGE", "WB", "NSE", "NSEModified"],
        )

        for i in range(len(gauges)):
            # get the index of the first value in the column that is not -9 or Nan
            st1 = df1.loc[:, df1.columns[i]][
                df1.loc[:, df1.columns[i]] != no_data_value
            ].index[0]
            st2 = df2.loc[:, df2.columns[i]][
                df2.loc[:, df2.columns[i]] != no_data_value
            ].index[0]

            metrics.loc[gauges[i], "start"] = max(st1, st2)
            end1 = df1[df1.columns[i]][df1[df1.columns[i]] != no_data_value].index[-1]
            end2 = df2[df2.columns[i]][df2[df2.columns[i]] != no_data_value].index[-1]
            metrics.loc[gauges[i], "end"] = min(end1, end2)

        # manually adjust and start or end date to calculate the performance between
        # two dates
        if start != "":
            metrics.loc[:, "start"] = dt.datetime.strptime(start, fmt)
        if end != "":
            metrics.loc[:, "end"] = dt.datetime.strptime(end, fmt)

        # calculate th metrics
        for i in range(len(gauges)):
            start_date = metrics.loc[gauges[i], "start"]
            end_date = metrics.loc[gauges[i], "end"]
            obs = df1.loc[start_date:end_date, gauges[i]].values.tolist()
            sim = df2.loc[start_date:end_date, gauges[i]].values.tolist()

            # shift hm result
            sim[shift:-shift] = sim[0 : -shift * 2]

            metrics.loc[gauges[i], "rmse"] = round(pf.rmse(obs, sim), 0)
            metrics.loc[gauges[i], "KGE"] = round(pf.kge(obs, sim), 3)
            metrics.loc[gauges[i], "NSE"] = round(pf.nse(obs, sim), 3)
            metrics.loc[gauges[i], "NSEModified"] = round(pf.nse_hf(obs, sim), 3)
            metrics.loc[gauges[i], "WB"] = round(pf.wb(obs, sim), 0)
            metrics.loc[gauges[i], "MBE"] = round(pf.mbe(obs, sim), 3)
            metrics.loc[gauges[i], "MAE"] = round(pf.mae(obs, sim), 3)

        return metrics

    def hm_vs_rrm(
        self, start: str = "", end: str = "", fmt: str = "%Y-%m-%d", shift: int = 0
    ):
        """hm_vs_rrm.

            hm_vs_rrm calculates the performance metrics between the hydraulic model simulated discharge and the
            rainfall-runoff model simulated discharge.

        Parameters
        ----------
        start: [str]
            the stating date for the period you want to calculate the error for.
        end: [str]
            the end date for the period you want to calculate the error for.
        fmt: [str]
            format of the given date
        shift: [int]
            if there is a shift in the calculated timeseries, by one or more time steps, and you want to fix this
            problem in calculating the metrics by shifting the calculated timeseries by one or more time steps.

        Returns
        -------
        MetricsHM_RRM: [dataframe]
            dataframe with the gauges id as rows and ['start', 'end', 'rmse', 'KGE', 'WB', 'NSE',
            'NSEModefied'], as columns.
        """
        if not isinstance(self.hm_gauges, DataFrame) and not isinstance(
            self.hm_gauges, GeoDataFrame
        ):
            raise ValueError(
                "rrm_gauges variable does not exist please read the RRM results with 'ReadRRM' method"
            )
        if not isinstance(self.rrm_gauges, list):
            raise ValueError(
                "rrm_gauges variable does not exist please read the RRM results with 'ReadRRM' method"
            )
        if not isinstance(self.q_rrm, DataFrame):
            raise ValueError("please read the RRM results with the 'ReadRRM' method")
        if not isinstance(self.q_hm, DataFrame):
            raise ValueError("please read the HM results with the 'ReadHMQ' method")
        # HM vs RRM
        self.metrics_hm_vs_rrm = self.metrics(
            self.q_rrm,
            self.q_hm,
            self.rrm_gauges,
            self.no_data_value,
            start,
            end,
            shift,
            fmt,
        )
        # get the point geometry from the hm_gauges
        self.metrics_hm_vs_rrm = self.hm_gauges.merge(
            self.metrics_hm_vs_rrm,
            left_on=self.gauge_id_col,
            right_index=True,
            how="left",
            sort=False,
        )
        self.metrics_hm_vs_rrm.index = self.metrics_hm_vs_rrm[self.gauge_id_col]
        self.metrics_hm_vs_rrm.index.name = "index"
        if isinstance(self.hm_gauges, GeoDataFrame):
            self.metrics_hm_vs_rrm.crs = self.hm_gauges.crs

    def rrm_vs_observed(
        self, start: str = "", end: str = "", fmt: str = "%Y-%m-%d", shift: int = 0
    ):
        """rrm_vs_observed.

            rrm_vs_observed calculates the performance metrics between the hydraulic model simulated discharge and
            the rainfall-runoff model simulated discharge.

        Parameters
        ----------
        start: [str]
            the stating date for the period you want to calculate the error for.
        end: [str]
            the end date for the period you want to calculate the error for.
        fmt: [str]
            format of the given date
        shift: [int]
            if there is a shift in the calculated timeseries by one or more time steps, and you want to fix this
            problem in calculating the metrics by shifting the calculated timeseries by one or more time steps.

        Returns
        -------
        MetricsHM_RRM: [dataframe]
            dataframe with the gauges id as rows and ['start', 'end', 'rmse', 'KGE', 'WB', 'NSE',
            'NSEModefied'], as columns.
        """
        if not isinstance(self.rrm_gauges, list):
            raise ValueError(
                "rrm_gauges variable does not exist please read the RRM results with 'ReadRRM' method"
            )
        if not isinstance(self.q_rrm, DataFrame):
            raise ValueError("please read the RRM results with the 'ReadRRM' method")

        if not isinstance(self.q_gauges, DataFrame):
            raise ValueError(
                "q_gauges variable does not exist please read the gauges data with 'ReadObservedQ' method"
            )

        # RRM vs observed
        self.metrics_rrm_vs_obs = self.metrics(
            self.q_gauges,
            self.q_rrm,
            self.rrm_gauges,
            self.no_data_value,
            start,
            end,
            shift,
            fmt,
        )

        self.metrics_rrm_vs_obs = self.hm_gauges.merge(
            self.metrics_rrm_vs_obs,
            left_on=self.gauge_id_col,
            right_index=True,
            how="left",
            sort=False,
        )

        self.metrics_rrm_vs_obs.index = self.metrics_rrm_vs_obs[self.gauge_id_col]
        self.metrics_rrm_vs_obs.index.name = "index"
        if isinstance(self.hm_gauges, GeoDataFrame):
            self.metrics_rrm_vs_obs.crs = self.hm_gauges.crs

    def hm_vs_observed_discharge(
        self,
        start: str = "",
        end: str = "",
        fmt: str = "%Y-%m-%d",
        shift: int = 0,
    ):
        """HMQvsObserved.

            hm_vs_observed_discharge calculates the performance metrics between the hydraulic model simulated
            discharge and the rainfall-runoff model simulated discharge.

        Parameters
        ----------
        start: [str]
            the stating date for the period you want to calculate the error for.
        end: [str]
            the end date for the period you want to calculate the error for.
        fmt: [str]
            format of the given date
        shift: [int]
            if there is a shift in the calculated timeseries by one or more time steps, and you want to fix this
            problem in calculating the metrics by shifting the calculated timeseries by one or more time steps.

        Returns
        -------
        metrics_hm_q_vs_obs: [dataframe]
            dataframe with the gauges id as rows and ['start', 'end', 'rmse', 'KGE', 'WB', 'NSE',
            'NSEModefied'], as columns.
        """
        if not isinstance(self.q_gauges, DataFrame):
            raise ValueError(
                "q_gauges variable does not exist please read the gauges' data with 'ReadObservedQ' method"
            )

        if not isinstance(self.q_hm, DataFrame):
            raise ValueError(
                "q_hm variable does not exist please read the HM results with 'ReadHMQ' method"
            )

        # HM Q vs observed
        self.metrics_hm_q_vs_obs = self.metrics(
            self.q_gauges,
            self.q_hm,
            self.discharge_gauges_list,
            self.no_data_value,
            start,
            end,
            shift,
            fmt,
        )

        self.metrics_hm_q_vs_obs = self.hm_gauges.merge(
            self.metrics_hm_q_vs_obs,
            left_on=self.gauge_id_col,
            right_index=True,
            how="left",
            sort=False,
        )

        self.metrics_hm_q_vs_obs.index = self.metrics_hm_q_vs_obs[self.gauge_id_col]
        self.metrics_hm_q_vs_obs.index.name = "index"
        if isinstance(self.hm_gauges, GeoDataFrame):
            self.metrics_hm_q_vs_obs.crs = self.hm_gauges.crs

    def hm_vs_observed_water_level(
        self,
        start: str = "",
        end: str = "",
        fmt: str = "%Y-%m-%d",
        shift: int = 0,
    ):
        """hm_vs_observed_water_level.

            hm_vs_observed_water_level calculates the performance metrics between the hydraulic model simulated
            discharge and the rainfall-runoff model simulated discharge.

        Parameters
        ----------
        start: [str]
            the stating date for the period you want to calculate the error for.
        end: [str]
            the end date for the period you want to calculate the error for.
        fmt: [str]
            format of the given date
        shift: [int]
            if there is a shift in the calculated timeseries by one or more time steps, and you want to fix this
            problem in calculating the metrics by shifting the calculated timeseries by one or more time steps.

        Returns
        -------
        metrics_hm_wl_vs_obs: [dataframe]
            dataframe with the gauges id as rows and ['start', 'end', 'rmse', 'KGE', 'WB', 'NSE',
            'NSEModefied'], as columns.
        """
        if not isinstance(self.wl_gauges, DataFrame):
            raise ValueError(
                "wl_gauges variable does not exist please read the water level gauges with 'readObservedWL' method"
            )

        if not isinstance(self.wl_hm, DataFrame):
            raise ValueError(
                "wl_hm variable does not exist please read the water level simulated by the HM with 'readHMWL' method"
            )

        # HM WL vs observed
        self.metrics_hm_wl_vs_obs = self.metrics(
            self.wl_gauges,
            self.wl_hm,
            self.wl_gauges_list,
            self.no_data_value,
            start,
            end,
            shift,
            fmt,
        )

        self.metrics_hm_wl_vs_obs = self.hm_gauges.merge(
            self.metrics_hm_wl_vs_obs,
            left_on=self.gauge_id_col,
            right_index=True,
            how="left",
            sort=False,
        )

        self.metrics_hm_wl_vs_obs.index = self.metrics_hm_wl_vs_obs[self.gauge_id_col]
        self.metrics_hm_wl_vs_obs.index.name = "index"
        if isinstance(self.hm_gauges, GeoDataFrame):
            self.metrics_hm_wl_vs_obs.crs = self.hm_gauges.crs

    def inspect_gauge(
        self,
        reach_id: int,
        gauge_id: int = 0,
        start: str = "",
        end: str = "",
        fmt: str = "%Y-%m-%d",
    ) -> Union[
        tuple[DataFrame, Figure, tuple[Any, Any]], tuple[DataFrame, Figure, Any]
    ]:
        """inspect_gauge.

            inspect_gauge returns the metrices of the simulated discharge and water level and plots it.

        Parameters
        ----------
        reach_id: [int]
            river reach id
        gauge_id: [int]
            if the river reach has more than one gauge, gauge_id is the gauge order.
        start: [str]
            start date, if not given, it will be taken from the already calculated Metrics table.
        end: [str]
            end date, if not given, it will be taken from the already calculated Metrics table.
        fmt : [str]
            format of the given dates. The default is "%Y-%m-%d".

        Returns
        -------
        summary: [DataFrame]
            performance metrix
        """
        if not isinstance(self.metrics_hm_vs_rrm, DataFrame) and not isinstance(
            self.metrics_hm_vs_rrm, GeoDataFrame
        ):
            raise ValueError(
                "please calculate first the metrics_hm_vs_rrm by the method HMvsRRM"
            )

        gauge = self.get_gauges(reach_id, gauge_id)
        gauge_id = gauge.loc[0, self.gauge_id_col]
        gauge_name = str(gauge.loc[0, "name"])

        summary = pd.DataFrame(
            index=["HM-RRM", "RRM-Observed", "HM-Q-Observed", "HM-WL-Observed"],
            columns=self.metrics_hm_vs_rrm.columns,
        )
        # for each gauge in the reach
        if isinstance(self.metrics_hm_q_vs_obs, DataFrame) or isinstance(
            self.metrics_hm_q_vs_obs, GeoDataFrame
        ):
            summary.loc["HM-Q-Observed", :] = self.metrics_hm_q_vs_obs.loc[gauge_id, :]

        if gauge.loc[0, "waterlevel"] == 1 and gauge.loc[0, "discharge"] == 1:
            fig, (ax1, ax2) = plt.subplots(
                ncols=1, nrows=2, sharex=True, figsize=(15, 8)
            )
        else:
            fig, ax1 = plt.subplots(ncols=1, nrows=1, figsize=(15, 8))

        if gauge_id in self.rrm_gauges:
            # there are RRM simulated data
            summary.loc["HM-RRM", :] = self.metrics_hm_vs_rrm.loc[gauge_id, :]
            if isinstance(self.metrics_rrm_vs_obs, DataFrame) or isinstance(
                self.metrics_rrm_vs_obs, GeoDataFrame
            ):
                summary.loc["RRM-Observed", :] = self.metrics_rrm_vs_obs.loc[
                    gauge_id, :
                ]

            if start == "":
                start_1 = self.metrics_hm_vs_rrm.loc[gauge_id, "start"]
            else:
                s1 = dt.datetime.strptime(start, fmt)
                s2 = self.metrics_hm_vs_rrm.loc[gauge_id, "start"]
                start_1 = max(s1, s2)

            if end == "":
                end_1 = self.metrics_hm_vs_rrm.loc[gauge_id, "end"]
            else:
                e1 = dt.datetime.strptime(end, fmt)
                e2 = self.metrics_hm_vs_rrm.loc[gauge_id, "end"]
                end_1 = min(e1, e2)

            ax1.plot(self.q_hm[gauge_id].loc[start_1:end_1], label="HM", zorder=5)
            ax1.plot(self.q_gauges[gauge_id].loc[start_1:end_1], label="Observed")
            ax1.plot(self.q_rrm[gauge_id].loc[start_1:end_1], label="RRM")
            ax1.set_ylabel("Discharge m3/s", fontsize=12)
            ax1.legend(fontsize=15)
            # SimMax = max(self.q_hm[gauge_id].loc[start:end])
            # ObsMax = max(self.q_rrm[gauge_id].loc[start:end])
            # pos = max(SimMax, ObsMax)
        if gauge.loc[0, "waterlevel"] == 1:
            # there are water level observed data
            summary.loc["HM-WL-Observed", :] = self.metrics_hm_wl_vs_obs.loc[
                gauge_id, :
            ]

            if start == "":
                start_2 = self.metrics_hm_wl_vs_obs.loc[gauge_id, "start"]
            else:
                s1 = dt.datetime.strptime(start, fmt)
                s2 = self.metrics_hm_wl_vs_obs.loc[gauge_id, "start"]
                start_2 = max(s1, s2)

            if end == "":
                end_2 = self.metrics_hm_wl_vs_obs.loc[gauge_id, "end"]
            else:
                e1 = dt.datetime.strptime(end, fmt)
                e2 = self.metrics_hm_wl_vs_obs.loc[gauge_id, "end"]
                end_2 = min(e1, e2)

            ax2.plot(self.wl_hm[gauge_id].loc[start_2:end_2], label="HM", linewidth=2)
            ax2.plot(
                self.wl_gauges[gauge_id].loc[start_2:end_2],
                label="Observed",
                linewidth=2,
            )
            ax2.set_ylabel("Water Level m", fontsize=12)
            ax2.legend(fontsize=15)

            # SimMax = max(self.wl_hm[gauge_id].loc[start_2:end_2])
            # ObsMax = max(self.wl_gauges[gauge_id].loc[start_2: end_2])
            # pos = max(SimMax, ObsMax)
        # plt.legend(font_size=15)
        ax1.set_title(gauge_name, fontsize=30)
        ax1.set_title(gauge_name, fontsize=30)

        if gauge.loc[0, "waterlevel"] == 1:
            return summary, fig, (ax1, ax2)
        else:
            return summary, fig, ax1

    @staticmethod
    def prepare_to_save(df: DataFrame) -> DataFrame:
        """prepare_to_save.

            prepare_to_save convert all the dates in the dataframe into string.

        Parameters
        ----------
        df: [dataframe]
            the
        Returns
        -------
        Dataframe
        """
        df.drop(["start", "end"], axis=1, inplace=True)
        if "Qstart" in df.columns.tolist():
            start = df["Qstart"].tolist()
        else:
            start = df["WLstart"].tolist()

        for i in range(len(start)):
            if "Qstart" in df.columns.tolist():
                if isinstance(df.loc[df.index[i], "Qstart"], Timestamp):
                    df.loc[df.index[i], "Qstart"] = str(
                        df.loc[df.index[i], "Qstart"].date()
                    )
                if isinstance(df.loc[df.index[i], "Qend"], Timestamp):
                    df.loc[df.index[i], "Qend"] = str(
                        df.loc[df.index[i], "Qend"].date()
                    )

            if "WLstart" in df.columns.tolist():
                if isinstance(df.loc[df.index[i], "WLstart"], Timestamp):
                    df.loc[df.index[i], "WLstart"] = str(
                        df.loc[df.index[i], "WLstart"].date()
                    )
                if isinstance(df.loc[df.index[i], "WLend"], Timestamp):
                    df.loc[df.index[i], "WLend"] = str(
                        df.loc[df.index[i], "WLend"].date()
                    )
        return df

    def save_metrices(self, path):
        """save_metrices.

            save_metrices saves the calculated metrics.

        Parameters
        ----------
        path: [str]

        Returns
        -------
        None
        """
        if isinstance(self.metrics_hm_vs_rrm, GeoDataFrame) or isinstance(
            self.metrics_hm_vs_rrm, DataFrame
        ):
            df = self.prepare_to_save(self.metrics_hm_vs_rrm.copy())
            if isinstance(self.metrics_hm_vs_rrm, GeoDataFrame):
                df.to_file(path + "MetricsHM_Q_RRM.geojson", driver="GeoJSON")
            if isinstance(self.metrics_hm_vs_rrm, DataFrame):
                df.to_csv(path + "MetricsHM_Q_RRM.geojson.csv")

        if isinstance(self.metrics_hm_q_vs_obs, GeoDataFrame) or isinstance(
            self.metrics_hm_q_vs_obs, DataFrame
        ):
            df = self.prepare_to_save(self.metrics_hm_q_vs_obs.copy())
            if isinstance(self.metrics_hm_q_vs_obs, GeoDataFrame):
                df.to_file(path + "MetricsHM_Q_Obs.geojson", driver="GeoJSON")
            if isinstance(self.metrics_hm_q_vs_obs, DataFrame):
                df.to_csv(path + "MetricsHM_Q_Obs.geojson.csv")

        if isinstance(self.metrics_rrm_vs_obs, GeoDataFrame) or isinstance(
            self.metrics_rrm_vs_obs, DataFrame
        ):
            df = self.prepare_to_save(self.metrics_rrm_vs_obs.copy())
            if isinstance(self.metrics_rrm_vs_obs, GeoDataFrame):
                df.to_file(path + "MetricsRRM_Q_Obs.geojson", driver="GeoJSON")
            if isinstance(self.metrics_rrm_vs_obs, DataFrame):
                df.to_csv(path + "MetricsRRM_Q_Obs.geojson.csv")

        if isinstance(self.metrics_hm_wl_vs_obs, GeoDataFrame) or isinstance(
            self.metrics_hm_wl_vs_obs, DataFrame
        ):
            df = self.prepare_to_save(self.metrics_hm_wl_vs_obs.copy())
            if isinstance(self.metrics_hm_wl_vs_obs, GeoDataFrame):
                df.to_file(path + "MetricsHM_WL_Obs.geojson", driver="GeoJSON")
            if isinstance(self.metrics_hm_wl_vs_obs, DataFrame):
                df.to_csv(path + "MetricsHM_WL_Obs.geojson.csv")
