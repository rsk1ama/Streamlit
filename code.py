import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title="Dashboard monitor anodizing", layout="wide")


upload_file = st.file_uploader ("Upload file excel" , type=["xlsx"])
if  upload_file:
    #read file excel        
    df = pd.read_excel(upload_file)
    df.columns = df.columns.str.strip()
    df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], errors='coerce', infer_datetime_format = True)
    df.dropna(subset = ['TIMESTAMP'], inplace=True) 
    df.set_index('TIMESTAMP', inplace=True)
    df.replace(0,np.nan, inplace = True)
    st.subheader("เลือกช่วงเวลา")
    min_date = df.index.min().date()
    max_date = df.index.max().date()
    start_date, end_date = st.date_input("ช่วงวันที่" , [min_date , max_date] , min_value = min_date , max_value = max_date)
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1)
    df_range = df.loc[(df.index >= start_dt) & (df.index < end_dt)]
    if df_range.empty:
        st.warning("ไม่พบช่วงเวลาข้อมูล")
    else:
        st.success(f"พบข้อมูล{len(df_range)} แถว")
        with st.expander("แสดงข้อมูลในช่วงเวลา"):
            st.subheader("Data")
            st.dataframe(df_range)
           
    cols = st.columns(10)
    sensor_clicked = None
    sensor_list = ['Temperature 1', 'Temperature 2', 'Temperature 3' , 'Temperature 4', 'Temperature 5', 'Temperature 6' , 'Temperature 7' , 
        'Flowlate chemical' , 'Pr.Suction chemical' , 'Pr.Dischange chemical']
    for i , col in enumerate(cols):
        with col:
            if st.button(f"Sensor {i+1}"):
                sensor_clicked = sensor_list[i]
    if sensor_clicked:
        st.subheader(f"แสดงกราฟ:{sensor_clicked}")
        fig = px.line(df_range , x = df_range.index , y = sensor_clicked)
        st.plotly_chart(fig , use_container_width=True)






































    
            
        
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
          