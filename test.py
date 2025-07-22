import streamlit as st
import pandas as pd
from PIL import Image
import base64
from io import BytesIO
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
                st.rerun()
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
        st.rerun()

    st.set_page_config(page_title="Dashboard monitor anodizing", layout="wide")


    required_columns = ["Temperature 1","Temperature 2","Temperature 3","Temperature 4","Temperature 5","Temperature 6",
    "Temperature 7","Flowlate chemical","Pr.Suction chemical","Pr.Dischange chemical"]



        # Load CSV data
    df = pd.read_csv("History.csv", parse_dates=["TIMESTAMP"],dayfirst= True)
    df = df.dropna(subset=required_columns)    
    df.columns = df.columns.str.strip()
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce")
    df = df.sort_values("TIMESTAMP")
    latest = df.iloc[-1]
    df.replace([0,65505,65535],np.nan, inplace = True)

            # Load layout image
    bg_image = Image.open("scada_layout_real.png")
    st.set_page_config(layout="wide")
    st.title("🖥️ Dashboard")



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

        # Sensor values
    temps = [latest[f"Temperature {i}"] for i in range(1, 8)]
    flow = latest["Flowlate chemical"]
    pr_suction = latest["Pr.Suction chemical"]
    pr_discharge = latest["Pr.Dischange chemical"]

        # Load icons
    temp_icon = Image.open("icons/temp_icon.png")
    flow_icon = Image.open("icons/flow_icon.png")
    pressure_icon = Image.open("icons/pressure_icon.png")

        # Convert image to base64
    def image_to_base64(img):
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode()

        # Position (x, y) in pixel (adjust as needed to match layout)
    positions = {
            "Temp1": (393, 225),
            "Temp2": (493, 225),
            "Temp3": (583, 225),
            "Temp4": (673, 225),
            "Temp5": (773, 225),
            "Temp6": (863, 225),
            "Temp7": (963, 225),
            "Flow": (575, 80),
            "Pr.Suction": (800, 20),
            "Pr.Dischange": (800, 80),
        }

        # Draw HTML/CSS overlay
    st.markdown(f"""
            <style>
            .container {{
                position: relative;
                width: 100%;
                max-width: 1400px;
                margin: auto;
                height: auto;    
            }}
            .bg {{
                width: 100%;
                display: block;
            }}
            .sensor {{
                position: absolute;
                z-index: 10;
                text-align: center;
                font-weight: bold;
            
            }}
            </style>


            <div class="container">
            <img class="bg" src="data:image/png;base64,{image_to_base64(bg_image)}"/>

            <!-- Temperature sensors -->
            {"".join([
            f'''
            <div class="sensor" style="top:{positions[f'Temp{i+1}'][1]}px; left:{positions[f'Temp{i+1}'][0]}px">
                <img src="data:image/png;base64,{image_to_base64(temp_icon)}" width="32"/><br>
                <span style="color:{'red' if temps[i] > 70 else 'black'}">{temps[i]:.1f} °C</span>
            </div>
            ''' for i in range(7)
            ])}

            <!-- Flow sensor -->
            <div class="sensor" style="top:{positions['Flow'][1]}px; left:{positions['Flow'][0]}px">
                <img src="data:image/png;base64,{image_to_base64(flow_icon)}" width="32"/><br>
                <span style="color:{'red' if flow < 130 else 'black'}">{flow:.1f} l/min</span>
            </div>

            <!-- Pressure sensors -->
            <div class="sensor" style="top:{positions['Pr.Suction'][1]}px; left:{positions['Pr.Suction'][0]}px">
                <img src="data:image/png;base64,{image_to_base64(pressure_icon)}" width="32"/><br>
                <span>{pr_suction:.1f} bar</span>
            </div>
            <div class="sensor" style="top:{positions['Pr.Dischange'][1]}px; left:{positions['Pr.Dischange'][0]}px">
                <img src="data:image/png;base64,{image_to_base64(pressure_icon)}" width="32"/><br>
                <span style="color:{'red' if pr_discharge < 300 else 'black'}">{pr_discharge:.1f} kPa</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    cols = st.columns(10)
    sensor_clicked = None
    sensor_list = ['Temperature 1', 'Temperature 2', 'Temperature 3' , 'Temperature 4', 'Temperature 5', 'Temperature 6' , 'Temperature 7' , 
                    'Flowlate chemical' , 'Pr.Suction chemical' , 'Pr.Dischange chemical']
    if 'sensor_clicked' not in st.session_state:
            st.session_state['senor_clicked'] = None
    for i , col in enumerate(cols):
            with col:
                if st.button(sensor_list[i]):
                
                    st.session_state['sensor_clicked'] = sensor_list[i]
    sensor_clicked = st.session_state.get('sensor_clicked', None)
    if sensor_clicked:    
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
            sensor_data = df[mask][["TIMESTAMP",sensor_clicked]].dropna(subset=[sensor_clicked])

            if sensor_data.empty:
                    st.warning("no data for date")
                    st.stop()
            if sensor_clicked in sensor_thresholds:

                    warning = sensor_thresholds[sensor_clicked]["warning"]
                    immediate = sensor_thresholds[sensor_clicked]["immediate"]
                    print("Warning =", warning)    
                    print("Immediate =", immediate)
                                    
                                        #chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x = sensor_data["TIMESTAMP"],
                y = sensor_data[sensor_clicked],
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
                title = f"ค่าที่วัดได้จาก : {sensor_data}",
                xaxis_title ="เวลา",
                yaxis_title ="ค่า",
                hovermode ="x unified",
                legend_title ="ข้อมูล",
                )
            
            st.plotly_chart(fig,use_container_width=True)
            with st.expander("ดูข้อมูล"):
                st.dataframe(sensor_data,use_container_width=True)
                    









