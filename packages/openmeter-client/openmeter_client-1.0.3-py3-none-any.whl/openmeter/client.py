import json
import requests  # type: ignore
import pandas as pd  # type: ignore

from loguru import logger


class OpenMeterClient:
    """
    Api class to handle get, post and patch requests of openmeter api, base_url is set to
    v1 version right now, for more info see https://api.openmeter.de/v1/docs.

    Args:
        :access_token (str): access_token of the client

    Example 1:
        One could use the demo token or a personal access token generated from https://appstore.logarithmo.de/app/openmeterplatform/v1/demo/page-interface
        Please note that demo token has limitations and is only for quick testing

        .. code-block:: python

            >>> om_client = OpenMeterClient(personal_access_token=your_personal_access_token)
            >>> demo_client = OpenMeterClient(personal_access_token="969AC556-9185-48B2-97D2-D72341911067")

            For all the examples here after, om_client and demo_client will be used interchangebly.

    """

    def __init__(self, personal_access_token: str):
        """
        Initializes an instance of the OpenMeterClient class and checks if the api is live.

        Args:
            :personal_access_token (str): The personal access token for authentication.

        """
        self.base_url = "https://api.openmeter.de/v1"
        self._api_key = personal_access_token

    @property
    def api_key(self):
        """
        property to get the api key of the client.

        Returns:
            :api_key (str): The api key of the client.
        """
        return self._api_key

    def api_status(self):
        """
        method to get the current status of https://api.openmeter.de/v1/docs

        Returns:
            :api_status (str): Returns OK if the api is live, otherwise ERROR.
        """
        local_params = {
            "access_token": self._api_key,
        }
        url = self.base_url + "/docs"
        result = requests.get(url, params=local_params)
        if result.status_code == 200:
            logger.info(f"Api is live with status code {str(result.status_code)}")
            return "OK"
        else:
            logger.error(f"Api is down with status code {str(result.status_code)}")
            logger.error(str(result.text))
            return "ERROR"

    def test_request_status(self, result):
        """
        generalized method to test the result status for exceptions.

        Args:
            :result: the response of the requests.get, requests.post....etc..

        Returns:
            :result: the response of the requests.get, requests.post....etc..
        """
        try:
            result.raise_for_status()
        except Exception as exc:
            if exc.request.method == 'GET' and 'timeseries?' in exc.request.url and result.text == '{"detail":"Item(s) not found"}':
                logger.info(f"timeseries data retrieved for {int(exc.request.url[-1]) if int(exc.request.url[-1])> 0 else 0} pages")
            else:
                logger.info(str(exc))
        return result

    def get_meta_data(
        self,
        sensor_id: str = None,
        private_id: str = None,
        location_id: str = None,
        energy_type: str = None,
        measurement_category: str = None,
        measurement_type: str = None,
        measurement_unit: str = None,
        measurement_value_type: str = None,
        measurement_frequency: str = None,
        country: str = None,
        federal_state: str = None,
        city: str = None,
        post_code: str = None,
        category: str = None,
        usage: str = None,
        usage_detail: str = None,
        page: int = None,
    ):
        """
        Retrieve the meta data of sensors based on conditional filters, for detailed instructions
        visit https://api.openmeter.de/v1/docs#/Meta%20Data/read_meta_data_meta_data_get

        Args:
            :sensor_id (str): The sensor ID.
            :private_id (str): The private ID.
            :location_id (str): The location ID.
            :energy_type (str): The energy type.
            :measurement_category (str): The measurement category.
            :measurement_type (str): The measurement type.
            :measurement_unit (str): The measurement unit.
            :measurement_value_type (str): The measurement value type.
            :measurement_frequency (str): The measurement frequency.
            :country (str): The country.
            :federal_state (str): The federal state.
            :city (str): The city.
            :post_code (str): The postal code.
            :category (str): The category.
            :usage (str): The usage.
            :usage_detail (str): The usage detail.
            :page (int): The page number.

        Returns:
            pandas.DataFrame: The meta data of filtered sensors.

        Example 1:
            In the following example we retrieve the meta data of a single sensor using the sensor id directly and
            print measurement_type, unit and frequency.

            .. code-block:: python

                >>> sensor_id = "78347197-77dc-4861-ae1f-19f21a6ff510"
                >>> meter_data = demo_client.get_meta_data(sensor_id=sensor_id)
                >>> print(meter_data[["measurement_type", "measurement_unit", "measurement_frequency"]])
                measurement_type measurement_unit measurement_frequency
                0       Wirkarbeit              kWh                 15min

                >>> print(meter_data.filter(like="location"))
                                            location_id  ... location_latitude
                0  4603629f-ac04-4f38-b3e2-54b98615db83  ...          51.19193

        Example 2:
            Filtering the sensors based on multiple conditions to do analysis on a group of sensors, as you can
            observe from the filtered_sensors dataframe info, metadata for most sensors is available, one could
            also build filters using a combination of sensor metadata and location attributes to make more meaningful
            analysis of sensors of interest

            .. code-block:: python

                >>> filtered_sensors = demo_client.get_meta_data(energy_type="Strom", measurement_frequency="24h")
                >>> print(filtered_sensors.info())
                <class 'pandas.core.frame.DataFrame'>
                RangeIndex: 2252 entries, 0 to 2251
                Data columns (total 30 columns):
                #   Column                      Non-Null Count  Dtype
                ---  ------                      --------------  -----
                0   id                          2252 non-null   object
                1   created_at                  2252 non-null   object
                2   updated_at                  2252 non-null   object
                3   measures_from               2078 non-null   object
                4   measures_to                 2078 non-null   object
                5   measures_count              0 non-null      object
                6   energy_type                 2252 non-null   object
                7   measurement_category        2252 non-null   object
                8   measurement_type            2252 non-null   object
                9   measurement_unit            2252 non-null   object
                10  measurement_value_type      2252 non-null   object
                11  measurement_frequency       2252 non-null   object
                12  notes                       118 non-null    object
                13  private_id                  0 non-null      object
                14  measurement_timezone        2252 non-null   object
                15  location_id                 2252 non-null   object
                16  location_created_at         2252 non-null   object
                17  location_updated_at         2252 non-null   object
                18  location_country            2252 non-null   object
                19  location_federal_state      2252 non-null   object
                20  location_city               2251 non-null   object
                21  location_post_code          2250 non-null   float64
                22  location_category           2252 non-null   object
                23  location_usage              2232 non-null   object
                24  location_usage_detail       564 non-null    object
                25  location_area               2084 non-null   float64
                26  location_construction_year  573 non-null    float64
                27  location_private_id         0 non-null      object
                28  location_longitude          2202 non-null   float64
                29  location_latitude           2202 non-null   float64
                dtypes: float64(5), object(25)
                memory usage: 527.9+ KB

        """
        local_params = {
            "access_token": self._api_key,
            "sensor_id": sensor_id,
            "private_id": private_id,
            "location_id": location_id,
            "energy_type": energy_type,
            "measurement_category": measurement_category,
            "measurement_type": measurement_type,
            "measurement_unit": measurement_unit,
            "measurement_value_type": measurement_value_type,
            "measurement_frequency": measurement_frequency,
            "country": country,
            "federal_state": federal_state,
            "city": city,
            "post_code": post_code,
            "category": category,
            "usage": usage,
            "usage_detail": usage_detail,
            "page": page,
        }

        local_params = {
            key: value for key, value in local_params.items() if value is not None
        }

        # list to collect the results of multiple pages
        results_list = []

        if local_params.get("page") is None:
            local_params["page"] = 0

            while True:
                result = requests.get(f"{self.base_url}/meta_data", params=local_params)
                result = self.test_request_status(result)
                result = json.loads(result.text)
                result_data = result["data"]
                results_list.extend(result_data)

                if not result["information"]["next_page_query"]:
                    break
                local_params["page"] = local_params["page"] + 1
        else:
            result = requests.get(f"{self.base_url}/meta_data", params=local_params)
            result = self.test_request_status(result)
            result = json.loads(result.text)
            result_data = result["data"]
            results_list.extend(result_data)

        df = pd.DataFrame(results_list)
        location_df = pd.json_normalize(df["location"]).add_prefix("location_")
        df = pd.concat([df, location_df], axis=1)
        df = df.drop(columns=["location"])
        return df

    def post_meta_data(self, sensor_meta_data: dict, location_id: str = None):
        """
        method to create a new sensor, provides the functionality to attach an existing
        location object to a new sensor being created, if no location_id is being provided,
        then the meta_data dictionary needs to contain location information, for detailed
        instructions visit https://api.openmeter.de/v1/docs#/Meta%20Data/write_meta_data_meta_data_post

        Args:
            :sensor_meta_data: the meta data information of a new sensor
            :location_id: Optional, if provided, needs to be in the database.

        Returns:
            dict: a nested dictionary containing the sensor metadata along with the id of sensor
            and location(new/existing) information is returned.

        Example 1:
            For instance, if one is creating a new sensor and a new location, it's necessary to provide the
            metadata of the sensor and also the location information together as follows, the returned response
            consists of the new sensor and location ids generated along with customer information, please save the
            sensor ids for retrieving the information later using get_meta_data method

            .. code-block:: python

                >>> test_metadata = {
                        "energy_type": "Strom",
                        "measurement_category": "Verbrauch",
                        "measurement_type": "Wirkarbeit (Brennwert)",
                        "measurement_unit": "kWh(Hs)",
                        "measurement_value_type": "Zaehlerstand",
                        "measurement_frequency": "24h",
                        "notes": "This sensor was newly installed in 2022",
                        "private_id": "string",
                        "measurement_timezone": "Europe_Berlin",
                        "location": {
                            "country": "Deutschland",
                            "federal_state": "Baden-Wuerttemberg",
                            "city": "string",
                            "post_code": 0,
                            "category": "Gewerblich",
                            "usage": "string",
                            "usage_detail": "string",
                            "area": 230.5,
                            "construction_year": 1970,
                            "private_id": "string",
                        }
                    }
                >>> response_post = om_client.post_meta_data(sensor_meta_data=test_metadata)
                >>> print(response_post)
                {'id': 'c8abf795-39fc-4d3f-a05d-0ca6f590bc27', 'created_at': '2023-12-21T13:06:38.578186+00:00', 'updated_at': '2023-12-21T13:06:38.578208+00:00',
                'measures_from': None, 'measures_to': None, 'measures_count': None, 'energy_type': 'Strom', 'measurement_category': 'Verbrauch',
                'measurement_type': 'Wirkarbeit (Brennwert)', 'measurement_unit': 'kWh(Hs)', 'measurement_value_type': 'Zaehlerstand',
                'measurement_frequency': '24h', 'notes': 'This sensor was newly installed in 2022', 'private_id': 'string', 'measurement_timezone': 'Europe_Berlin',
                'customer': {'name': 'Some User', 'email': 'newuseremail@gmail.com', 'role': 'USER'},
                'location': {'id': '86ab8bd5-1776-4185-b0dd-73da667cc914', 'created_at': '2023-12-21T13:06:38.577427+00:00', 'updated_at': '2023-12-21T13:06:38.577522+00:00',
                'country': 'Deutschland', 'federal_state': 'Baden-Wuerttemberg', 'city': 'string', 'post_code': 0, 'category': 'Gewerblich', 'usage': 'string',
                'usage_detail': 'string', 'area': 230.5, 'construction_year': 1970, 'private_id': 'string', 'longitude': 0.0, 'latitude': 0.0}}

        Example 2:
            There may be cases where you already created a sensor with a location, and you would like to use the same location for other new sensors,
            to handle this scenario, one could use the location_id attribute directly instead of passing a nested location object in the metadata, here's a simple
            example case where the location_id obtained from the previous post request is being used here to create another sensor

            .. code-block:: python

                >>> test_metadata = {
                        "energy_type": "Strom",
                        "measurement_category": "Verbrauch",
                        "measurement_type": "Wirkarbeit",
                        "measurement_unit": "kWh",
                        "measurement_value_type": "Differenzmengenwert",
                        "measurement_frequency": "24h",
                        "notes": "energy consumption",
                        "private_id": "sensor_home_2022",
                        "measurement_timezone": "Europe_Berlin",
                    }
                >>> response_post = om_client.post_meta_data(sensor_meta_data=test_metadata, location_id="86ab8bd5-1776-4185-b0dd-73da667cc914")

                The response would be same as above with the existing location linked to the new sensor.

        """
        local_params = {
            "access_token": self._api_key,
        }

        if location_id:
            local_params.update({"location_id": location_id})
        result = requests.post(
            f"{self.base_url}/meta_data", params=local_params, json=sensor_meta_data
        )
        result = self.test_request_status(result)
        result = json.loads(result.text)
        return result

    def patch_meta_data(self, sensor_id: str, sensor_meta_data: dict):
        """
        method to update metadata of an existing sensor, location data of a sensor
        can also be updated, for detailed instructions please visit
        https://api.openmeter.de/v1/docs#/Meta%20Data/update_meta_data_meta_data_patch

        Args:
            :sensor_id: id of an existing sensor.
            :sensor_meta_data: the dictionary with the updated information fields.

        Returns:
            dict: containing information of update status of sensor.

        Example 1:
            Updating sensor and location information to correct errors is possible using the patch_metadata method
            it's also flexible to just provide the information of the attributes you'd like to update which leaves the
            rest of the attributes as is in the database, in the following example, the changes are only being made in the
            attributes energy_type, measurement_type, measurement_unit, measurement_value_type and measurement_frequency

            .. code-block:: python

                >>> patch_metadata = {
                        "energy_type": "Wasser",
                        "measurement_type": "Wassermenge",
                        "measurement_unit": "kW",
                        "measurement_value_type": "Differenzmengenwert",
                        "measurement_frequency": "15min",
                    }
                >>> response_patch = om_client.patch_meta_data(sensor_id="c8abf795-39fc-4d3f-a05d-0ca6f590bc27", sensor_meta_data=patch_metadata)
                >>> print(response_patch)
                {'detail': 'Meta Data updates accepted for sensor id - c8abf795-39fc-4d3f-a05d-0ca6f590bc27'}

        Example 2:
            It's also possible to update location information using the same method, here's a case where the updates are being made to location object as well
            to change the federal_state and category of a location object

            .. code-block:: python

                >>> patch_metadata = {
                        "energy_type": "Wasser",
                        "measurement_category": "Verbrauch",
                        "measurement_type": "Wassermenge",
                        "measurement_unit": "kW",
                        "measurement_value_type": "Differenzmengenwert",
                        "measurement_frequency": "15min",
                        "location": {
                            "federal_state": "Bayern",
                            "category": "Privat",
                        }
                    }
                >>> response_patch = om_client.patch_meta_data(sensor_id="c8abf795-39fc-4d3f-a05d-0ca6f590bc27", sensor_meta_data=patch_metadata)
                >>> print(response_patch)
                {'detail': 'Meta Data updates accepted for sensor id - c8abf795-39fc-4d3f-a05d-0ca6f590bc27'}

            please note that patch method doesn't return the metadata of the sensor but the status itself, you could use the get_meta_data method to validate the updates

        """
        local_params = {"access_token": self._api_key, "sensor_id": sensor_id}
        result = requests.patch(
            f"{self.base_url}/meta_data", params=local_params, json=sensor_meta_data
        )
        result = self.test_request_status(result)
        result = json.loads(result.text)
        return result

    def get_meta_data_distinct(self, attribute_name: str):
        """
        method to read the unique values of the metadata attributes, for detailed instructions
        visit https://api.openmeter.de/v1/docs#/Meta%20Data/read_attributes_meta_data_distinct_values_get

        Args:
            :attribute_name: the name of the metadata field.

        Returns:
            list: a list of unique values of the metadata field.

        Example 1:
            Some attributes have restrictions on the possible values for an attribute to standardize the metadata, use this method for reading
            the current possible values

            .. code-block:: python

                >>> measurement_types = om_client.get_meta_data_distinct(attribute_name="measurement_type")
                >>> print(measurement_types)
                ['Blindleistung', 'Wassermenge', 'bereitgestellte Leistung', 'Wirkleistung', 'Blindarbeit', 'Wirkarbeit (Brennwert)', 'Brennstoffmenge', 'Wirkarbeit']
                >>> measurement_units = om_client.get_meta_data_distinct(attribute_name="measurement_unit")
                >>> print(measurement_units)
                ['kVArh', 'kWh', 'm³', 'kW', 'kWh(Hs)', 'kVAr', 'MWh']

        """
        local_params = {"access_token": self._api_key, "attribute_name": attribute_name}
        result = requests.get(
            f"{self.base_url}/meta_data/distinct_values", params=local_params
        )
        result = self.test_request_status(result)
        result = json.loads(result.text)
        if "detail" in result:
            logger.error(result["detail"])
            return None
        return result["available_expressions"]

    def get_timeseries(
        self,
        sensor_id: str,
        from_timestamp: pd.Timestamp = None,
        to_timestamp: pd.Timestamp = None,
    ):
        """
        method to retrieve timeseries data for a given sensor, for detailed instructions
        please visit https://api.openmeter.de/v1/docs#/Timeseries/read_timeseries_timeseries_get

        Args:
            :sensor_id: id of an existing sensor
            :from_timestamp: Optional, timestamp from which data is to retrieved
            :to_timestamp: Optional, timestamp to which data is to retrieved

        Returns:
            pandas.DataFrame: a dataframe containing the timeseries data of the sensor.

        Example 1:
            To retrieve all the timeseries data of a particular sensor

            .. code-block:: python

                >>> chosen_sensor_id = '78347197-77dc-4861-ae1f-19f21a6ff510'
                >>> ts_data = om_client.get_timeseries(sensor_id=chosen_sensor_id)
                >>> print(ts_data)
                                    timestamps  values
                0     2000-01-01 01:00:00+01:00    0.20
                1     2000-01-01 02:00:00+01:00    0.20
                2     2000-01-01 03:00:00+01:00    0.20
                3     2000-01-01 04:00:00+01:00    0.20
                4     2000-01-01 05:00:00+01:00    0.20
                ...                         ...     ...
                23276 2023-12-10 23:00:00+01:00  108.55
                23277 2023-12-10 23:15:00+01:00   27.15
                23278 2023-12-10 23:30:00+01:00   27.10
                23279 2023-12-10 23:45:00+01:00   27.15
                23280 2023-12-11 00:00:00+01:00  108.75

                [323291 rows x 2 columns]

        Example 2:
            To retrieve the timeseries data of a particular sensor between any two dates

            .. code-block:: python

                >>> import pandas as pd
                >>> from_ts = pd.Timestamp("2020-01-01 00:00:00")
                >>> to_ts = pd.Timestamp("2023-12-31 23:59:59")

                >>> chosen_sensor_id = '78347197-77dc-4861-ae1f-19f21a6ff510'
                >>> ts_data = om_client.get_timeseries(sensor_id=chosen_sensor_id, from_timestamp=from_ts, to_timestamp=to_ts)
                >>> print(ts_data)
                                    timestamps  values
                0    2020-01-01 01:00:00+01:00   28.70
                1    2020-01-01 01:15:00+01:00   28.45
                2    2020-01-01 01:30:00+01:00   28.30
                3    2020-01-01 01:45:00+01:00   28.50
                4    2020-01-01 02:00:00+01:00   28.35
                ...                        ...     ...
                3038 2023-12-10 23:00:00+01:00  108.55
                3039 2023-12-10 23:15:00+01:00   27.15
                3040 2023-12-10 23:30:00+01:00   27.10
                3041 2023-12-10 23:45:00+01:00   27.15
                3042 2023-12-11 00:00:00+01:00  108.75

                [123047 rows x 2 columns]

        """
        # list to collect the results of multiple pages
        results_list = []

        local_params = {
            "access_token": self._api_key,
            "sensor_id": sensor_id,
            "from_ts": from_timestamp,
            "to_ts": to_timestamp,
            "page": 0,
        }

        while True:
            try:
                result = requests.get(
                    f"{self.base_url}/timeseries", params=local_params
                )
                result = self.test_request_status(result)
                result = json.loads(result.text)
                # result_info = result["information"]
                result_data = result["data"]
                results_list.append(result_data)

                if not result["information"]["next_page_query"]:
                    break
                local_params["page"] = local_params["page"] + 1
            except KeyError as e:
                assert result["detail"] == "Item(s) not found"
                break

        timeseries_list = [pd.DataFrame(page) for page in results_list]
        timeseries_df = pd.concat(timeseries_list) if len(timeseries_list) > 0 else pd.DataFrame(columns=["timestamps", "values"])
        timeseries_df['timestamps'] = pd.to_datetime(timeseries_df['timestamps']).dt.tz_localize('UTC')
        timeseries_df['timestamps'] = timeseries_df['timestamps'].dt.tz_convert('Europe/Berlin')
        return timeseries_df

    def post_timeseries(self, sensor_id: str, timeseries_data: dict):
        """
        method to add/update timeseries data of an existing sensor, for detailed instructions
        please visit https://api.openmeter.de/v1/docs#/Timeseries/write_timeseries_timeseries_post

        Args:
            :sensor_id: id of an existing sensor
            :timeseries_data: dictionary object containing separate lists for
                timestamps and values.

        Returns:
            requests.Response: the response object of the post request informing
            the status of updates.

        Example 1:

            To add timeseries data of a sensor, the timestamps and values have to be of the same length as follows,
            also please note that to update the data as well, the same method can be used.

            .. code-block:: python

                >>> sensor_id = "c8abf795-39fc-4d3f-a05d-0ca6f590bc27"
                >>> data = {
                        "timestamps": [
                            "2022-01-01 15:00:00",
                            "2022-01-01 15:15:00",
                            "2022-01-01 15:30:00"
                        ],
                        "values": [
                            18,
                            20,
                            22
                        ]
                    }
                >>> post_ts_response = om_client.post_timeseries(sensor_id=sensor_id, timeseries_data=data)
                >>> print(post_ts_response)
                {'detail': 'Timeseries Data updates accepted for sensor id - c8abf795-39fc-4d3f-a05d-0ca6f590bc27'}

                The easiest way to validate the updates is to use the get_timeseries method

        """

        local_params = {
            "access_token": self._api_key,
            "sensor_id": sensor_id,
        }

        result = requests.post(
            f"{self.base_url}/timeseries", params=local_params, json=timeseries_data
        )
        result = self.test_request_status(result)
        result = json.loads(result.text)
        return result

    def get_timeseries_weather(
        self,
        location_id: str,
        weather_type: str,
        from_timestamp: pd.Timestamp = None,
        to_timestamp: pd.Timestamp = None,
    ):
        """
        method to retrieve weather data for a given location of a sensor, for detailed instructions
        please visit https://api.openmeter.de/v1/docs#/Weather/read_timeseries_weather_timeseries_weather_get

        Args:
            :location_id: location id of an existing sensor
            :weather_type: weather type to retrieve
            :from_timestamp: Optional, timestamp from which data is to retrieved
            :to_timestamp: Optional, timestamp to which data is to retrieved

        Returns:
            pandas.DataFrame: a dataframe containing the chosen weather data closest to the sensor.

        Example 1:
            To retrieve all the available wind timeseries data of a particular location

            .. code-block:: python

                >>> chosen_location_id = '4603629f-ac04-4f38-b3e2-54b98615db83'
                >>> wind_data = om_client.get_timeseries_weather(location_id=chosen_location_id, weather_type="wind")
                >>> print(wind_data)
                                    timestamps  values
                0      2016-01-30T01:00:00+01:00    11.0
                1      2016-01-30T02:00:00+01:00    10.7
                2      2016-01-30T03:00:00+01:00    10.9
                3      2016-01-30T04:00:00+01:00    10.6
                4      2016-01-30T05:00:00+01:00    10.6
                ...                          ...     ...
                68721  2023-12-10T19:00:00+01:00     7.7
                68722  2023-12-10T20:00:00+01:00     8.8
                68723  2023-12-10T21:00:00+01:00     8.0
                68724  2023-12-10T22:00:00+01:00    10.3
                68725  2023-12-10T23:00:00+01:00     9.4

                [68726 rows x 2 columns]

        Example 2:
            To retrieve all the available solar timeseries data of a particular location

            .. code-block:: python

                >>> chosen_location_id = '4603629f-ac04-4f38-b3e2-54b98615db83'
                >>> solar_data = om_client.get_timeseries_weather(location_id=chosen_location_id, weather_type="solar")
                >>> print(solar_data)
                                     timestamps  values
                0     2023-09-01T02:00:00+02:00     0.0
                1     2023-09-01T03:00:00+02:00     0.0
                2     2023-09-01T04:00:00+02:00     0.0
                3     2023-09-01T05:00:00+02:00     0.0
                4     2023-09-01T06:00:00+02:00     0.0
                ...                         ...     ...
                2179  2023-11-30T20:00:00+01:00     0.0
                2180  2023-11-30T21:00:00+01:00     0.0
                2181  2023-11-30T22:00:00+01:00     0.0
                2182  2023-11-30T23:00:00+01:00     0.0
                2183  2023-12-01T00:00:00+01:00     0.0

                [2184 rows x 2 columns]

        Example 3:
            To retrieve all the available temperature timeseries data of a particular location

            .. code-block:: python

                >>> chosen_location_id = '4603629f-ac04-4f38-b3e2-54b98615db83'
                >>> temperature_data = om_client.get_timeseries_weather(location_id=chosen_location_id, weather_type="temperature")
                >>> print(temperature_data)
                                    timestamps  values
                0       1999-12-31T23:00:00+01:00     4.3
                1       2000-01-01T00:00:00+01:00     4.2
                2       2000-01-01T01:00:00+01:00     4.3
                3       2000-01-01T02:00:00+01:00     4.3
                4       2000-01-01T03:00:00+01:00     4.5
                ...                           ...     ...
                209802  2023-12-10T19:00:00+01:00     9.4
                209803  2023-12-10T20:00:00+01:00     8.4
                209804  2023-12-10T21:00:00+01:00     9.7
                209805  2023-12-10T22:00:00+01:00    11.2
                209806  2023-12-10T23:00:00+01:00    11.1

                [209807 rows x 2 columns]

        Example 4:
            To retrieve the available weather timeseries data for a particular location
            between the dates of interest, the same logic applies to all weather_type attributes

            .. code-block:: python

                >>> import pandas as pd
                >>> from_ts = pd.Timestamp("2020-01-01 00:00:00")
                >>> to_ts = pd.Timestamp("2023-12-31 23:59:59")

                >>> chosen_location_id = '4603629f-ac04-4f38-b3e2-54b98615db83'
                >>> temperature_data = om_client.get_timeseries_weather(location_id=chosen_location_id, weather_type="temperature", from_timestamp=from_ts, to_timestamp=to_ts)
                >>> print(temperature_data)
                                    timestamps  values
                0      2020-01-01T00:00:00+01:00     1.7
                1      2020-01-01T01:00:00+01:00     1.1
                2      2020-01-01T02:00:00+01:00     1.1
                3      2020-01-01T03:00:00+01:00     0.8
                4      2020-01-01T04:00:00+01:00     0.0
                ...                          ...     ...
                34724  2023-12-20T20:00:00+01:00     8.2
                34725  2023-12-20T21:00:00+01:00     8.3
                34726  2023-12-20T22:00:00+01:00     8.2
                34727  2023-12-20T23:00:00+01:00     8.1
                34728  2023-12-21T00:00:00+01:00     8.2

                [34729 rows x 2 columns]

        """

        local_params = {
            "access_token": self._api_key,
            "location_id": location_id,
            "weather_type": weather_type,
            "from_ts": from_timestamp,
            "to_ts": to_timestamp,
        }

        try:
            result = requests.get(
                f"{self.base_url}/timeseries_weather", params=local_params
            )
            result = self.test_request_status(result)
            result = json.loads(result.text)
            # result_info = result["information"]
            result_data = result["data"]
            return pd.DataFrame(result_data)
        except KeyError as e:
            assert result["detail"] == "Item(s) not found"
            return pd.DataFrame()

    def get_all_sensors_from_same_location(
        self, sensor_id: str = None, location_id: str = None
    ):
        """
        Example method to retrives similar sensors based on a query sensor_id or location_id,
        only one of the two parameters can be provided.

        Args:
            :sensor_id: sensor id of an existing sensor
            :location_id: location id of an existing sensor

        Returns:
            pandas.DataFrame: The meta data of filtered sensors.
        """

        if sensor_id and location_id:
            assert False, "Please provide either sensor_id or location_id"

        if not location_id:
            _location_id = self.get_meta_data(sensor_id=sensor_id)
            if not _location_id:
                assert False, "No sensor found with the provided sensor_id"
            _location_id = _location_id[0]
        else:
            _location_id = location_id

        return self.get_meta_data(location_id=_location_id)
