import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


st.set_page_config(page_title="Dashboard monitor anodizing", layout="wide")


        
df = pd.read_excel("HistoryData.xlsx")
df.columns = df.columns.str.strip()
df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors='coerce', infer_datetime_format = True)
df.replace([0,65505,65535],np.nan, inplace = True)
       
sensor_thresholds = {
        
    "Temperature 1" : {"warning": 70, "immediate": 90},
    "Temperature 2" : {"warning": 70, "immediate": 90},
    "Temperature 3" : {"warning": 70, "immediate": 90},
    "Temperature 4" : {"warning": 70, "immediate": 90},
    "Temperature 5" : {"warning": 70, "immediate": 90},
    "Temperature 6" : {"warning": 70, "immediate": 90},
    "Temperature 7" : {"warning": 70, "immediate": 90},
    "Flowlate chemical" : {"warning": 130, "immediate": 100},
    "Pr.Suction chemical": {"warning": 250, "immediate": 200},
    "Pr.Dischange chemical": {"warning": 250, "immediate": 200}
    }
           
available_sensors = [s for s in sensor_thresholds if s in df.columns]
if not available_sensors:
    st.error()
    sensor = st.selectbox("เลือก sensor", available_sensors)

    st.subheader("เลือกช่วงเวลา")
    min_date = df["TIMESTAMP"].min().date()
    max_date = df["TIMESTAMP"].max().date()
    start_date, end_date = st.date_input("ช่วงวันที่" , [min_date , max_date] , min_value = min_date , max_value = max_date)
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date) + pd.Timedelta(days=1)

    
if start_date > end_date:
   st.error("ไม่พบช่วงเวลาข้อมูล")
else:
   mask = (df["TIMESTAMP"].dt.date >= start_date) & (df["TIMESTAMP"].dt.date <= end_date)
   sensor_data = df.loc[mask,["TIMESTAMP",sensor]].dropna()

   if sensor_data.empty:
        st.warning("no data for date")
        st.stop()
warning = sensor_thresholds[sensor]["warning"]
immediate = sensor_thresholds[sensor]["immediate"]
print("Warning =", warning)    
print("Immediate =", immediate)
    

fig = go.Figure()
fig.add_trace(go.Scatter(
    x = sensor_data["TIMESTAMP"],
    y = sensor_data[sensor],
    mode="lines",
    name= "ค่าที่วัดได้",
    line=dict(color="blue") ))
    

fig.add_trace(go.Scatter(
    x = [sensor_data["TIMESTAMP"].min(),sensor_data["TIMESTAMP"].max()],
    y = [warning, warning],
    mode="lines",
    name= "Warning",
    line=dict(color="orange",dash="dash") ))
    
fig.add_trace(go.Scatter(
    x = [sensor_data["TIMESTAMP"].min(),sensor_data["TIMESTAMP"].max()],
    y = [immediate, immediate],
    mode="lines",
    name= "Immediate",
    line=dict(color="red",dash="dot") ))
    
    
fig.update_layout(
    title = f"ค่าที่วัดได้จาก : {sensor}",
    xaxis_title ="เวลา",
    yaxis_title ="ค่า",
    hovermode ="x unified",
    legend_title ="ข้อมูล",
    )
    
st.plotly_chart(fig,use_container_width=True)
with st.expander("ดูข้อมูล"):
        st.dataframe(sensor_data,use_container_width=True)





































    
            
        
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
          
