import pandas as pd
import numpy as np


# load dataset
def wrangle_data_fun():
    path_to_data = "model/airline-safety.csv"
    data = pd.read_csv(path_to_data)
    # add incidents/accidents/fatalities for both time periods together
    data["total_incidents"] = data["incidents_85_99"] + data["incidents_00_14"]

    # calculate available seat km per week in billions
    data["avail_seat_km_per_week_billions"] = data["avail_seat_km_per_week"] / 1000000000

    # include only airlines that had incidents
    no_zeros = data[data["incidents_85_99"] > 0]
    no_zeros_either = no_zeros[no_zeros["incidents_00_14"] > 0]
    # create dataset to use for plot2 
    data2 = no_zeros_either
    data2["fatalities_85_99"] = data2["fatalities_85_99"] / data2["avail_seat_km_per_week_billions"]
    data2["fatalities_00_14"] = data2["fatalities_00_14"] / data2["avail_seat_km_per_week_billions"]
    data2["total_fatalities_per_b_avail_seat_km"] = data2["fatalities_85_99"] + data2["fatalities_00_14"]
    data2 = data2.reset_index().drop(columns="index")

    # classify first world countries based on https://www.nationsonline.org/oneworld/first_world.htm
    data2["first_world"] = np.zeros(len(data2))
    data2["first_world"] = "Other"
    data2["first_world"][
        3, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 22, 23, 24, 28, 30, 32, 34, 36, 40, 41, 42] = "First World"

    # create data set for boxplot
    data3 = no_zeros_either
    data3["lethality_85_99"] = data3["fatal_accidents_85_99"] / data3["incidents_85_99"]
    data3["lethality_00_14"] = data3["fatal_accidents_00_14"] / data3["incidents_00_14"]
    leathality_data = pd.melt(data3,
                              id_vars="airline",
                              value_vars=["lethality_85_99",
                                          "lethality_00_14"],
                              var_name="lethality_period",
                              value_name="lethality_value")

    fatal_data = pd.melt(no_zeros_either,
                         id_vars="airline",
                         value_vars=["fatalities_85_99",
                                     "fatalities_00_14"],
                         var_name="fatalities_period",
                         value_name="fatalities_value").dropna()
    # data2["fatalities_period"], data2["fatalities_value"] = data3["fatalities_period"], data3["fatalities_value"]
    incident_data = pd.melt(no_zeros_either,
                            id_vars="airline",
                            value_vars=["incidents_85_99", "incidents_00_14"],
                            var_name="incident_period",
                            value_name="incident_value")

    lethal_incidents_data = pd.melt(no_zeros_either,
                                    id_vars="airline",
                                    value_vars=["fatal_accidents_85_99", "fatal_accidents_00_14"],
                                    var_name="fatal_accident_period",
                                    value_name="fatal_accident_value")

    hist_data = pd.merge(leathality_data, fatal_data, on="airline")
    hist_data = pd.merge(hist_data, incident_data, on="airline")
    hist_data = pd.merge(hist_data, lethal_incidents_data, on="airline")
    return data2, hist_data


chart_2_data, chart_1_data = wrangle_data_fun()
