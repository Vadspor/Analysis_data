import pandas as pd
import os
import streamlit as st
import webbrowser
import numpy as np
import time


vocabulary_of_provinces = {"Cherkasy": 22, "Chernihiv": 24, "Chernivtsi": 23, "Crimea": 25, "Dnipropetrovs'k": 3,
                           "Donets'k": 4, "Ivano-Frankivs'k": 8, "Kharkiv": 19, "Kherson": 20, "Khmel'nyts'kyy": 21,
                           "Kiev": 9, "Kiev City": 26, "Kirovohrad": 10, "Luhans'k": 11, "L'viv": 12, "Mykolayiv": 13,
                           "Odessa": 14, "Poltava": 15, "Rivne": 16, "Sevastopol'": 27, "Sumy": 17, "Ternopil'": 18,
                           "Transcarpathia": 6, "Vinnytsya": 1, "Volyn": 2, "Zaporizhzhya": 7, "Zhytomyr": 5}

index_of_province = {value: key for key, value in vocabulary_of_provinces.items()}

def FullDataVHI():
    full_provinces = []
    for province in os.listdir("provinces/"):
        full_provinces.append(f"provinces/{province}")
    df = pd.read_csv(full_provinces[0], sep=";")
    for i in range(1, len(full_provinces)):
        df = pd.concat([df, pd.read_csv(full_provinces[i], sep=";")], ignore_index=True)
    return df

def ResetP():
    st.session_state.scol = "VHI"
    st.session_state.sare = "Vinnytsya"
    st.session_state.dare = "Volyn"
    st.session_state.years = (1982, 2025)
    st.session_state.weeks = (1, 52)
    # st.session_state.sty = 1982
    # st.session_state.endy = 2025
    # st.session_state.stw = 1
    # st.session_state.endw = 52

st.title("Advanced Data Visualization")

df = FullDataVHI()

if "scol" not in st.session_state:
    st.session_state.scol = "VHI"
if "sare" not in st.session_state:
    st.session_state.sare = "Vinnytsya"
if "dare" not in st.session_state:
    st.session_state.dare = "Volyn"
if "years" not in st.session_state:
    st.session_state.years = (1982, 2025)
if "weeks" not in st.session_state:
    st.session_state.weeks = [1, 52]
if "sortrise" not in st.session_state:
    st.session_state.sortrise = False
if "sortfall" not in st.session_state:
    st.session_state.sortfall = False
# if "stw" not in st.session_state:
#     st.session_state.stw = 1
# if "endw" not in st.session_state:
#     st.session_state.endw = 52


st.sidebar.selectbox("Оберіть Стовпець", options=sorted(list(df.columns[4:-1])), key="scol")


regs = []
for index in sorted(list(df.area.unique())):
    regs.append(index_of_province[index])

st.sidebar.selectbox("Оберіть область", options=regs, key="sare")
sare = vocabulary_of_provinces[st.session_state.sare]

st.sidebar.slider("Select Years", min_value=1982, max_value=2025, value=[1982, 2025], key="years")
st.sidebar.slider("Select weeks", min_value=1, max_value=52, value=[1, 52], key="weeks")

# st.write(st.session_state.years, st.session_state.weeks)

# print(st.session_state.stw, st.session_state.endw)

st.sidebar.button("Скинути налаштування", on_click=ResetP)


# if st.sidebar.button("Скинути налаштування"):
    # for key in list(st.session_state.keys()):
    #     del st.session_state[key]
    # st.rerun()
    # print(st.session_state.scol, st.session_state.sare, st.session_state.sty, st.session_state.endy, st.session_state.stw, st.session_state.endw)
    # st.session_state.scol = "VHI"
    # st.session_state.sare = 1
    # st.session_state.sty = 1982
    # st.session_state.endy = 2025
    # st.session_state.stw = 1
    # st.session_state.endw = 52
    # print(st.session_state.scol, st.session_state.sare, st.session_state.sty, st.session_state.endy, st.session_state.stw, st.session_state.endw)
    # st.session_state.clear()
    # st.rerun()
    # webbrowser.open(st.get_url(), new=2)

df = df.sort_values(["area", "year", "week"]).reset_index(drop=True)


if st.session_state.years[1] == 2025 and st.session_state.weeks[1] > 9:
    df25 = df[df.year == 2025]
    df25 = df25[df25.week.between(st.session_state.weeks[0], 9)]
    df24 = df[df.week.between(st.session_state.weeks[0], st.session_state.weeks[1])]
    df24 = df24[df24.year < 2025]
    df = pd.concat([df24, df25])
else:
    df = df[df.week.between(st.session_state.weeks[0], st.session_state.weeks[1])]

df = df[df.year.between(st.session_state.years[0], st.session_state.years[1])].reset_index(drop=True)

oplt = df[df.area == sare]
oplt = oplt[["year", "week", st.session_state.scol]].reset_index(drop=True)

tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік 1", "Графік 2"])


st.sidebar.checkbox("Сортувати за зростанням", value=st.session_state["sortrise"], key="sortrise")
st.sidebar.checkbox("Сортувати за спаданням", value=st.session_state["sortfall"], key="sortfall")

if st.session_state.sortrise and not st.session_state.sortfall:
    # st.write(st.session_state.sortrise)
    oplt = oplt.sort_values([st.session_state.scol]).reset_index(drop=True)

elif st.session_state.sortfall and not st.session_state.sortrise:
    # st.write(st.session_state.sortrise)
    oplt = oplt.sort_values([st.session_state.scol], ascending=False).reset_index(drop=True)


with tab1:
    st.write("Data", oplt)

with tab2:
    st.line_chart(oplt[[st.session_state.scol]])
    
with tab3:
    st.selectbox("Оберіть область для порівняння", options=regs, key="dare")
    difdf = oplt[st.session_state.scol].to_frame()
    difdif = df[st.session_state.scol][df.area == vocabulary_of_provinces[st.session_state.dare]].reset_index(drop=True)
    difdf = difdf.join(difdif, rsuffix=f'_{st.session_state.dare}', how='outer')
    st.line_chart(difdf)

    if st.button("Порівняти із усіма областями"):
        # st.write("Data", df)
        # fullplt = df[[st.session_state.scol, st.session_state.sare]].reset_index(drop=True)
        # fullplt = oplt.rename(columns={st.session_state.scol: f"{st.session_state.scol}_{st.session_state.sare}"})
        fullplt = oplt[st.session_state.scol].to_frame()
        # st.write("Data", fullplt)
        for i in range(1, df.area.max()+1):
            if i != sare:
                testdf = df[st.session_state.scol][df.area == i].reset_index(drop=True)
                # st.write("Data", testdf)
                fullplt = fullplt.join(testdf, rsuffix=f'_{index_of_province[i]}', how='outer')
                # st.write("Data", fullplt)
        # st.write("Data", fullplt)
        st.line_chart(fullplt)



# print(st.session_state)









