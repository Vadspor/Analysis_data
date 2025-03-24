import datetime
import pandas as pd
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import requests as req

# url=f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID=8&year1=1981&year2=2025&type=Mean"
# vhi_url = urllib.request.urlopen(url)
# html_text = vhi_url.read().decode('utf-8')
# write_text = re.sub(r"<[^>]+>", "", html_text)
# out = open("vhi_id_16.csv", "w")
# out.writelines(write_text)
# out.close()
# print("VHI is downloaded...")
# # data_reg = pd.read_csv("vhi_id_16.csv", index_col=False, header=1)
#
#
# data_reg = pd.read_csv("vhi_id_16.csv", sep=",", index_col=False, skiprows=1)
# data_reg.columns = data_reg.columns.str.strip()
# data_reg = data_reg.drop(data_reg.loc[data_reg["VHI"] == -1].index)
# data_reg["area"] = 8
# data_reg.to_csv("vhi_id_16_new.csv", sep=";", index=False)
#
# print(data_reg)
# print(list(data_reg.columns.values))
# print(data_reg.dtypes)
# print(data_reg.head())

def DownloadDataFrame():
    vocabulary_of_provinces = {"Cherkasy": 22, "Chernihiv": 24, "Chernivtsi": 23, "Crimea": 25, "Dnipropetrovs'k": 3, "Donets'k" : 4, "Ivano-Frankivs'k": 8, "Kharkiv": 19, "Kherson": 20, "Khmel'nyts'kyy": 21, "Kiev": 9, "Kiev City": 9, "Kirovohrad": 10, "Luhans'k": 11, "L'viv": 12, "Mykolayiv": 13, "Odessa": 14, "Poltava": 15, "Rivne": 16, "Sevastopol'": 25, "Sumy": 17, "Ternopil'": 18, "Transcarpathia": 6, "Vinnytsya": 1, "Volyn": 2, "Zaporizhzhya": 7, "Zhytomyr": 5}
    # list_of_provinces = []
    os.makedirs("provinces", exist_ok=True)
    for i in range(27):
        url=f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i+1}&year1=1981&year2=2025&type=Mean"
        res_html = req.get(url).content.decode()
        province_name = re.search(r"Province=\s*\d+:\s*([^,]+)", res_html).group(1)
        # list_of_provinces.append(province_name)
        path = f"provinces/{province_name}_{datetime.datetime.now().strftime("%H-%M_%d-%m-%Y")}.csv"
        province = open(path, "w")
        province.write(re.sub(r"<[^>]+>", "", res_html))
        province.close()
        fix = pd.read_csv(path, sep=",", index_col=False, skiprows=1)
        fix.columns = fix.columns.str.strip()
        fix = fix.drop(fix.loc[fix["VHI"] == -1].index)
        if province_name in vocabulary_of_provinces:
            fix["area"] = vocabulary_of_provinces[province_name]
        else:
            fix["area"] = f"problem, {i + 1}"
        print(fix.head())
        fix.to_csv(path, sep=";", index=False)


# DownloadDataFrame()



def LineVHIYearProvince(province, year):
    provinces = [file for file in os.listdir("provinces/") if province in file]
    province = f"provinces/{provinces[0]}"
    data_reg = pd.read_csv(province, sep=";", index_col="year")
    print(data_reg)
    sub_data_reg = data_reg.loc[data_reg.index == year]
    s_data_reg = sub_data_reg[["week", "VHI", "area"]]
    return s_data_reg


# print(LineVHIYearProvince("Chernivtsi", 1999))


# def FindExtremumYear(provinces, years):
#     full_provinces = []
#     for province in provinces:
#         for file in os.listdir("provinces/"):
#             if province in file:
#                 full_provinces.append(f"provinces/{file}")
#                 print(full_provinces)
#     data_reg = pd.read_csv(full_provinces[0], sep=";", index_col="year")
#     colums = ["VHI", "area"]
#     for i in range(1, len(full_provinces)):
#         data_reg = data_reg.join(pd.read_csv(full_provinces[i], sep=";", index_col="year"), rsuffix=f"_{i+1}")
#         colums.append(f"VHI_{i+1}")
#         colums.append(f"area_{i+1}")
#     data_reg = data_reg.loc[data_reg.index.isin(years)][colums]
#     print(data_reg)



def FindExtremumYear(provinces, years):
    full_provinces = []
    for province in provinces:
        for file in os.listdir("provinces/"):
            if province in file:
                full_provinces.append(f"provinces/{file}")
                print(full_provinces)
    data_reg = pd.read_csv(full_provinces[0], sep=";")
    for i in range(1, len(full_provinces)):
        data_reg = pd.concat([data_reg, pd.read_csv(full_provinces[i], sep=";")], ignore_index=True)
    data_reg = data_reg.loc[data_reg["year"].isin(years)][["year", "week", "VHI", "area"]]
    return f"Min: \n{data_reg.loc[data_reg.VHI.idxmin(), ["year", "week", "VHI", "area"]]}\n", f"Max: \n{data_reg.loc[data_reg.VHI.idxmax(), ["year", "week", "VHI", "area"]]}\n", f"Mean: \n{data_reg.VHI.mean()}\n", f"Median: \n{data_reg.VHI.median()}\n"


# for obj in FindExtremumYear(["Cherkasy", "Chernivtsi"], [1999, 2000, 2001]):
#     print(obj)
# for obj in FindExtremumYear(["Volyn", "Rivne", "L'viv"], [2020, 2021]):
#     print(obj)


def RangeYearProvince(provinces, years):
    full_provinces = []
    for province in provinces:
        for file in os.listdir("provinces/"):
            if province in file:
                full_provinces.append(f"provinces/{file}")
                print(full_provinces)
    data_prov = pd.read_csv(full_provinces[0], sep=";")
    for i in range(1, len(full_provinces)):
        data_prov = pd.concat([data_prov, pd.read_csv(full_provinces[i], sep=";")], ignore_index=True)
    data_prov = data_prov.loc[data_prov["year"].isin(years)][["year", "week", "VHI", "area"]]
    return data_prov

# print(RangeYearProvince(["Volyn", "Rivne", "L'viv"], [2020, 2021]))
# print(RangeYearProvince(["Cherkasy", "Chernivtsi"], [1999, 2000, 2001]))


def ExtremeDroughtsYear():
    full_provinces = []
    for province in os.listdir("provinces/"):
        full_provinces.append(f"provinces/{province}")
    df = pd.read_csv(full_provinces[0], sep=";")
    for i in range(1, len(full_provinces)):
        df = pd.concat([df, pd.read_csv(full_provinces[i], sep=";")], ignore_index=True)
    weeks_dro = df.loc[df.VHI <= 15].reset_index(drop=True)
    years_dro = weeks_dro.groupby('year')['area'].nunique()
    years_ext = years_dro[years_dro >= 5].index
    df_years_ext = weeks_dro[weeks_dro["year"].isin(years_ext)].groupby(['year', 'area'])['VHI'].mean().reset_index()
    return df_years_ext.sort_values(by=["year", "area"], ascending=[True, True]).reset_index(drop=True)


# print(ExtremeDroughtsYear())