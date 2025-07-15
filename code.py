import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Dashboard monitor anodizing", layout="wide")
upload_file = st.file_uploader ("Upload file excel" , type=["xlsx"])
if upload_file:
    #read file excel        
    df = pd.read_excel(upload_file)
    df.columns = df.columns.str.strip()
    df.replace([0,65505,65535],np.nan, inplace = True)


    if "TIMESTAMP" in df.columns and not df["TIMESTAMP"].isnull().all():
        df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"])

        st.subheader("เลือกช่วงเวลา")
        min_time = df["TIMESTAMP"].min().date()
        max_time = df["TIMESTAMP"].max().date()

        start_date, end_date = st.date_input("เลือกช่วงวันที่",value=[min_time , max_time] , min_value = min_time , max_value = max_time)
    
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1)
        df_filterd = df[(df["TIMESTAMP"] >= start_dt) & (df["TIMESTAMP"] < end_dt)]


#===Detial sensor
    sensor_thesholds = {
        "Temperature 1" : {"warning": 70, "immediate": 90},
        "Temperature 2" : {"warning": 70, "immediate": 90},
        "Temperature 3" : {"warning": 70, "immediate": 90},
        "Temperature 4" : {"warning": 70, "immediate": 90},
        "Temperature 5" : {"warning": 70, "immediate": 90},
        "Temperature 6" : {"warning": 70, "immediate": 90},
        "Temperature 7" : {"warning": 70, "immediate": 90},
        "Flowlate chemical" : {"warning": 130, "immediate": 100},
        "Pr.Suction chemical" : {"warning": 270, "immediate": 250},
        "Pr.Dischange chemical" : {"warning": 270, "immediate": 250},
        }

    selected_sensors = st.multiselect("เลือก sensor ที่ต้องการแสดง:" , options=list(sensor_thesholds.keys()),
    default=["Temperature 1","Temperature 2","Temperature 3",])


    #chart
    for sensor in selected_sensors:
        if sensor not in df.columns:
            st.warning(f"ไม่พบข้อมูล:{sensor}")
            continue
        sensor_data = df_filterd[["TIMESTAMP",sensor]].dropna()
        thresholds = sensor_thesholds[sensor]

        ymin = min(sensor_data[sensor].min(), thresholds["warning"],thresholds["immediate"]) -10
        ymax = max(sensor_data[sensor].max(), thresholds["warning"],thresholds["immediate"]) +10


        line = alt.Chart(sensor_data).mark_line(color="steelblue").encode(x = "TIMESTAMP:T", y= alt.Y (f"{sensor}:Q" , title="sensor Valve", scale = alt.Scale(domain=[ymin,ymax])) ,tooltip=["TIMESTAMP",sensor])
        warning_line = alt.Chart(pd.DataFrame({"y": [thresholds["warning"]]})).mark_rule(color="orange", strokeDash=[5,5]).encode(y="y")
        immediate_line = alt.Chart(pd.DataFrame({"y": [thresholds["immediate"]]})).mark_rule(color="red", strokeDash=[3,3]).encode(y="y")
        chart = (line + warning_line + immediate_line).properties(title = f"{thresholds} ({sensor})" , width = 800 , height = 500)

        st.altair_chart(chart , use_container_width=True)





































    
            
        
#        if  st.button("Temp.1"):
#            fig = px.line(df_range , x = df_range.index , y = 'Temperature 1')
#           st.plotly_chart(fig , use_container_width=True)
    
 #       if  st.button("Temp.2"):
 #           fig = px.line(df_range , x = df_range.index , y = 'Temperature 2')
  #          st.plotly_chart(fig , use_container_width=True)
   #
 #       if  st.button("Temp.3"):
 #           fig = px.line(df_range , x = df_range.index , y = 'Temperature 3')
 #           st.plotly_chart(fig , use_container_width=True)
    
 #       if  st.button("Temp.4"):
 #           fig = px.line(df_range , x = df_range.index , y = 'Temperature 4')
 #           st.plotly_chart(fig , use_container_width=True)
    
 #       if  st.button("Temp.5"):
 #           fig = px.line(df_range , x = df_range.index , y = 'Temperature 5')
  #          st.plotly_chart(fig , use_container_width=True)
  
 #       if  st.button("Temp.6"):
 #           fig = px.line(df_range , x = df_range.index , y = 'Temperature 6')
 #           st.plotly_chart(fig , use_container_width=True)
    
 #       if  st.button("Temp.7"):
 #           fig = px.line(df_range , x = df_range.index , y = 'Temperature 7')
 #           st.plotly_chart(fig , use_container_width=True)
          
