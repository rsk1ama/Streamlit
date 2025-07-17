import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

USER_CREDENTIALS = {
       "admin":"TEF4",
       "user": "pass"
}
def login():
       st.title("Login Page")
       username = st.text_input("Username")
       password = st.text_input("Password", type="password")
       if st.button("Login"):
              if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Login สำเร็จ: {username}")
              else:
                     st.error("Username หรือ password ไม่ถูกต้อง")
        
if "logged_in" not in st.session_state:
       st.session_state["logged_in"] = False
if not st.session_state["logged_in"]:
       login()
else:
       st.success(f"ยินดีต้อนรับ {st.session_state['username']}")
          if st.button("Logout"):
             st.session_state['logged_in'] = False
             st.experimental_rerun()


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
               "Pr.Dischange chemical": {"warning": 250, "immediate": 200},
               "Tranfer Loading": {"warning": 3, "immediate": 5},
               "Tranfer Unloading": {"warning": 3, "immediate": 5},
               "Conveyor Main": {"warning": 8, "immediate": 10},
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
