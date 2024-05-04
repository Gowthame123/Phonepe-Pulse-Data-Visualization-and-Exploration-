#----------------------------------------------------------Import part---------------------------------------------------------------------------
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import mysql.connector
import numpy as np
import pandas as pd
import plotly.express as px
import json
import requests
import matplotlib.pyplot as plt


#-------------------------------------------------------my sql connection ----------------------------------------------------------------------
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user='root',
    password='root',
    database = "phonepe_data")
cursor = mydb.cursor()


#-------------------------------------------------------streamlit part--------------------------------------------------------------------------
st.set_page_config(layout="wide")
img = Image.open(r"C:\Users\gowth\Downloads\project_phonepe\files\Phonepe-copy-1.jpg")
st.image(img, use_column_width=True)
selected = option_menu(None,
                       options = ["Home","Analysis","Insights","Contact"],
                       icons = ["house","bar-chart","toggles","at"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                               "nav-link-selected": {"background-color": "#6F36AD"}})

# ----------------------------------------------------HOME TAB--------------------------------------------------------------------------------------------
if selected == "Home":
    
    st.subheader(
            "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
    st.markdown("[DOWNLOAD APP](https://www.phonepe.com/app-download/)")
    st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
    st.subheader(':violet[Phonepe Pulse]:')
    st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')  # Add newline after typing text
    st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
    st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')

st.write("---")

#----------------------------------------------------- ANALYSIS TAB----------------------------------------------------------------------------
if selected == "Analysis":
    # Center the title
    st.markdown("<h1 style='text-align: center; color: violet;'>ANALYSIS</h1>", unsafe_allow_html=True)
    
    # Center the subheader
    st.markdown("<h2 style='text-align: center;'>Analysis done on the basis of All India, States, and Top categories between 2018 and 2023</h2>", unsafe_allow_html=True)
    select = option_menu(None,
                         options=["AGGREGATE", "MAP", "TOP" ],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                   "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})
    if select == "AGGREGATE":
        tab1, tab2, tab3 = st.tabs(["TRANSACTION","USER",'INSURANCE'])


        #                              -------------------- TRANSACTION TAB-------------------
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                in_tr_yr = st.selectbox('**Select Years**', ('2018', '2019', '2020', '2021', '2022', '2023'), key='in_tr_yr')
            with col2:
                in_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_tr_qtr')
            with col3:
                in_tr_tr_typ = st.selectbox('**Select Transaction type**',
                                            ('Recharge & bill payments', 'Peer-to-peer payments',
                                             'Merchant payments', 'Financial Services', 'Others'), key='in_tr_tr_typ')

            # Transaction Analysis bar chart query    
            cursor.execute(
                f"SELECT States, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_tab_qry_rslt = cursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(np.array(in_tr_tab_qry_rslt), columns=['State', 'Transaction_amount'])
            df_in_tr_tab_qry_rslt1 = df_in_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_tab_qry_rslt) + 1)))

            # Transaction Analysis table query
            cursor.execute(
                f"SELECT States, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt),
                                                      columns=['State', 'Transaction_count', 'Transaction_amount'])
            df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt) + 1)))

            # Transaction Analysis table query
            cursor.execute(
                f"SELECT States, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}' ORDER BY Transaction_amount DESC;")
            in_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt),
                                                      columns=['State', 'Transaction_count', 'Transaction_amount'])
            df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt) + 1)))
            
             # Total Transaction Amount table query
            cursor.execute(
                f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_am_qry_rslt = cursor.fetchall()
            df_in_tr_am_qry_rslt = pd.DataFrame(np.array(in_tr_am_qry_rslt), columns=['Total', 'Average'])
            df_in_tr_am_qry_rslt1 = df_in_tr_am_qry_rslt.set_index(['Average'])


            # Total Transaction Count table query
            cursor.execute(
                f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_co_qry_rslt = cursor.fetchall()
            df_in_tr_co_qry_rslt = pd.DataFrame(np.array(in_tr_co_qry_rslt), columns=['Total', 'Average'])
            df_in_tr_co_qry_rslt1 = df_in_tr_co_qry_rslt.set_index(['Average'])

            # GEO VISUALISATION
            # Drop a State column from df_in_tr_tab_qry_rslt
            df_in_tr_tab_qry_rslt.drop(columns=['State'], inplace=True)

            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()

            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt

            df_state_names_tra['Transaction_amount'] = df_in_tr_tab_qry_rslt

            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)

            # Read csv
            df_tra = pd.read_csv('State_trans.csv')
            
            # Geo plot
            fig_tra = px.choropleth(
                df_tra,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
                color_continuous_scale='thermal', title='Transaction Analysis')
            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_tra, use_container_width=True)

            # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
            df_in_tr_tab_qry_rslt1['State'] = df_in_tr_tab_qry_rslt1['State'].astype(str)
            df_in_tr_tab_qry_rslt1['Transaction_amount'] = df_in_tr_tab_qry_rslt1['Transaction_amount'].astype(float)
            df_in_tr_tab_qry_rslt1_fig = px.bar(df_in_tr_tab_qry_rslt1, x='State', y='Transaction_amount',
                                                color='Transaction_amount', color_continuous_scale='thermal',
                                                title='Transaction Analysis Chart', height=700, )
            df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_in_tr_tab_qry_rslt1_fig, use_container_width=True)

            # -------  /  All India Total Transaction calculation Table   /   ----  #
            st.header(':violet[Total calculation]')

            col4, col5 = st.columns(2)
            with col4:
                st.subheader(':violet[Transaction Analysis]')
                st.dataframe(df_in_tr_anly_tab_qry_rslt1)
            with col5:
                st.subheader(':violet[Transaction Amount]')
                st.dataframe(df_in_tr_am_qry_rslt1)
                st.subheader(':violet[Transaction Count]')
                st.dataframe(df_in_tr_co_qry_rslt1)


        #                             ------------------USER TAB--------------------------
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                in_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_us_yr')
            with col2:
                if in_us_yr == '2022':
                    in_us_qtr = st.selectbox('**Select Quarter**', ('1'), key='in_us_qtr')
                else:                       
                    in_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_us_qtr')
   

            # SQL Query

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY States;")
            in_us_tab_qry_rslt = cursor.fetchall()
            df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['State', 'User Count'])
            df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

            # User Analysis Bar chart query
            cursor.execute(f"SELECT Brands, SUM(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY Brands;")
            in_us_tab_qry_rslt_b = cursor.fetchall()
            df_in_us_tab_qry_rslt_b= pd.DataFrame(np.array(in_us_tab_qry_rslt_b), columns=['Brands', 'User Count'])
            df_in_us_tab_qry_rslt1_b = df_in_us_tab_qry_rslt_b.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt_b) + 1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}' ;")
            in_us_co_qry_rslt = cursor.fetchall()
            df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total', 'Average'])
            df_in_us_co_qry_rslt1 = df_in_us_co_qry_rslt.set_index(['Average'])  

             # GEO VISUALIZATION FOR USER

            # Drop a State column from df_in_us_tab_qry_rslt
            df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['User Count'] = df_in_us_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('State_user.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_user.csv')
            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='User Count',
                color_continuous_scale='thermal', title='User Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_use, use_container_width=True)

            # ----   /   All India User Analysis Bar chart   /     -------- #
            df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['State'].astype(str)
            df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
            df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1, x='State', y='User Count', color='User Count',
                                                color_continuous_scale='thermal', title='User Analysis Chart',
                                                height=700, )
            df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_in_us_tab_qry_rslt1_fig, use_container_width=True)

            # -----   /   All India Total User calculation Table   /   ----- #
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader(':violet[User Analysis]')
                st.dataframe(df_in_us_tab_qry_rslt1)
            with col4:
                st.subheader(':violet[User Count]')
                st.dataframe(df_in_us_co_qry_rslt1) 

            # Convert the 'User Count' column to int if it's not already
            df_in_us_tab_qry_rslt1_b['User Count'] = df_in_us_tab_qry_rslt1_b['User Count'].astype(int)

            # Create the pie chart
            pie_chart_fig = px.pie(df_in_us_tab_qry_rslt1_b, values='User Count', names='Brands', 
                                    title='User Brand Analysis Donut Chart', hole = 0.4)

            # Customize the layout
            pie_chart_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', width=800, height=600)

            # Display the pie chart
            st.plotly_chart(pie_chart_fig, use_container_width=True)

#                                   -------------AGGREGATED INSURANCE----------------------- 
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                agg_in_yr = st.selectbox('**Select Year**', ('2020', '2021', '2022', '2023'), key='agg_in_yr')
            with col2:
                if agg_in_yr == '2020':
                    agg_in_qtr = st.selectbox('**Select Quarter**', ('2', '3', '4'), key='agg_in_qtr')
                else:                       
                    agg_in_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='agg_in_qtr')


            # SQL Query

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(Insurance_amount) FROM aggregated_insurance WHERE Years = '{agg_in_yr}' AND Quarter = '{agg_in_qtr}' GROUP BY States;")
            agg_in_tab_qry_rslt = cursor.fetchall()
            df_agg_in_tab_qry_rslt = pd.DataFrame(np.array(agg_in_tab_qry_rslt), columns=['State', 'Insurance amount'])
            df_agg_in_tab_qry_rslt1 = df_agg_in_tab_qry_rslt.set_index(pd.Index(range(1, len(df_agg_in_tab_qry_rslt) + 1)))

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(Insurance_count) FROM aggregated_insurance WHERE Years = '{agg_in_yr}' AND Quarter = '{agg_in_qtr}' GROUP BY States;")
            agg_in_tab_qry_rslt_b = cursor.fetchall()
            df_agg_in_tab_qry_rslt_b= pd.DataFrame(np.array(agg_in_tab_qry_rslt_b), columns=['State', 'Insurance Count'])
            df_agg_in_tab_qry_rslt1_b = df_agg_in_tab_qry_rslt_b.set_index(pd.Index(range(1, len(df_agg_in_tab_qry_rslt_b) + 1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(Insurance_count), AVG(Insurance_count) FROM aggregated_insurance WHERE Years = '{agg_in_yr}' AND Quarter = '{agg_in_qtr}';")
            agg_in_co_qry_rslt = cursor.fetchall()
            df_agg_in_co_qry_rslt = pd.DataFrame(np.array(agg_in_co_qry_rslt), columns=['Total', 'Average'])
            df_agg_in_co_qry_rslt1 = df_agg_in_co_qry_rslt.set_index(['Average'])

             # GEO VISUALIZATION FOR USER

            # Drop a State column from df_in_us_tab_qry_rslt
            df_agg_in_tab_qry_rslt.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['Insurance amount'] = df_agg_in_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('State_in_amt.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_in_amt.csv')
            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='Insurance amount',
                color_continuous_scale='thermal', title='Insurance amount Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_use, use_container_width=True)

            # ----   /   All India User Analysis Bar chart   /     -------- #
            df_agg_in_tab_qry_rslt1['State'] = df_agg_in_tab_qry_rslt1['State'].astype(str)
            df_agg_in_tab_qry_rslt1['Insurance amount'] = df_agg_in_tab_qry_rslt1['Insurance amount'].astype(int)
            df_agg_in_tab_qry_rslt1_fig = px.bar(df_agg_in_tab_qry_rslt1, x='State', y='Insurance amount', color='Insurance amount',
                                                color_continuous_scale='thermal', title='Insurance Analysis Chart',
                                                height=700, )
            df_agg_in_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_agg_in_tab_qry_rslt1_fig, use_container_width=True)

            # ----   /   All Brands User Analysis Bar chart   /     -------- #
            df_agg_in_tab_qry_rslt1_b['State'] = df_agg_in_tab_qry_rslt1_b['State'].astype(str)
            df_agg_in_tab_qry_rslt1_b['Insurance Count'] = df_agg_in_tab_qry_rslt1_b['Insurance Count'].astype(int)
            df_agg_in_tab_qry_rslt1_b_fig = px.bar(df_agg_in_tab_qry_rslt1_b, x='State', y='Insurance Count', color='Insurance Count',
                                                color_continuous_scale='thermal', title='Insurance count Analysis Chart',
                                                height=700, )
            df_agg_in_tab_qry_rslt1_b_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_agg_in_tab_qry_rslt1_b_fig, use_container_width=True)            

            # -----   /   All India Total User calculation Table   /   ----- #
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader(':violet[Insurance Analysis]')
                st.dataframe(df_agg_in_tab_qry_rslt1)
            with col4:
                st.subheader(':violet[Insurance Count]')
                st.dataframe(df_agg_in_co_qry_rslt1)                                                
#--------------------------------------------------------Map TAB---------------------------------------------------------------------------
    if select == "MAP":
        tab3 ,tab4, tab5 = st.tabs(["TRANSACTION","USER",'INSURANCE' ])

        #                -----------------------------TRANSACTION TAB FOR MAP---------------------
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st_tr_st = st.selectbox('**Select State**', (
                    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal'), key='st_tr_st')
            with col2:
                st_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_tr_yr')
            with col3:
                st_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')

            #Transaction Analysis pie chart query
            cursor.execute(f"SELECT District, Transaction_amount FROM map_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
            st_tr_tab_pie_qry_rslt = cursor.fetchall()
            df_st_tr_tab_pie_qry_rslt = pd.DataFrame(np.array(st_tr_tab_pie_qry_rslt),
                                                     columns=['District', 'Transaction_amount'])
            df_st_tr_tab_pie_qry_rslt1 = df_st_tr_tab_pie_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_tr_tab_pie_qry_rslt) + 1)))


            # Convert data types if necessary
            df_st_tr_tab_pie_qry_rslt1['Transaction_amount'] = df_st_tr_tab_pie_qry_rslt1['Transaction_amount'].astype(float)

            # Create the pie chart
            pie_chart_fig = px.pie(df_st_tr_tab_pie_qry_rslt1, values='Transaction_amount', names='District', 
                                    title='Transaction Analysis by District')

            # Customize the layout if needed
            pie_chart_fig.update_layout(
                title_font=dict(size=33), 
                title_font_color='#AD71EF',
                font=dict(size=14),  # Set the font size for labels
                height=700,  # Set the height of the plot
                width=800)            
                     
            # Display the pie chart
            st.plotly_chart(pie_chart_fig, use_container_width=True) 

            #Transaction count Analysis pie chart query
            cursor.execute(f"SELECT District, Transaction_count FROM map_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
            st_ct_tab_pie_qry_rslt = cursor.fetchall()
            df_st_ct_tab_pie_qry_rslt = pd.DataFrame(np.array(st_ct_tab_pie_qry_rslt),
                                                     columns=['District', 'Transaction_count'])
            df_st_ct_tab_pie_qry_rslt1 = df_st_ct_tab_pie_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_ct_tab_pie_qry_rslt) + 1)))

            col4, col5 = st.columns(2)
            with col4:
                st.subheader(':violet[District via Transaction amount]')
                st.dataframe(df_st_tr_tab_pie_qry_rslt1)            
            with col5:
                st.subheader(':violet[District via Transaction count]')
                st.dataframe(df_st_ct_tab_pie_qry_rslt1)


            # Convert data types if necessary
            df_st_ct_tab_pie_qry_rslt1['Transaction_count'] = df_st_ct_tab_pie_qry_rslt1['Transaction_count'].astype(int)

            # Create the pie chart
            donot_chart_fig = px.bar(df_st_ct_tab_pie_qry_rslt1, y='Transaction_count', x='District', 
                                    title='Transaction Count Analysis by District')

            # Customize the layout if needed
            donot_chart_fig.update_layout(
                title_font=dict(size=33), 
                title_font_color='#AD71EF',
                font=dict(size=14),  # Set the font size for labels
                height=700,  # Set the height of the plot
                width=800)

            # Display the pie chart
            st.plotly_chart(donot_chart_fig, use_container_width=True)  

        #                      -------------------user TAB FOR STATE-------------------------------
        with tab4:
            col1, col2, col3 = st.columns(3)
            with col1:
                st_ur_st = st.selectbox('**Select State**', (
                    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal'), key='st_ur_st')
            with col2:
                st_ur_yr = st.selectbox('**Select Year**', ('2020', '2021', '2022', '2023'), key='st_ur_yr')
            with col3:   
                    st_ur_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_ur_qtr')

            #Transaction Analysis pie chart query
            cursor.execute(f"SELECT Districts, RegisteredUser FROM map_user WHERE States = '{st_ur_st}' AND Years = '{st_ur_yr}' AND Quarter = '{st_ur_qtr}';")
            st_in_tab_pie_qry_rslt = cursor.fetchall()
            # Check if data is empty before creating DataFrame
 
            df_st_in_tab_pie_qry_rslt = pd.DataFrame(np.array(st_in_tab_pie_qry_rslt),
                                                    columns=['District', 'RegisteredUser'])
            df_st_in_tab_pie_qry_rslt1 = df_st_in_tab_pie_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_in_tab_pie_qry_rslt) + 1)))


            # Convert data types if necessary
            df_st_in_tab_pie_qry_rslt1['RegisteredUser'] = df_st_in_tab_pie_qry_rslt1['RegisteredUser'].astype(int)

            # Create the pie chart
            pie_chart_figg = px.pie(df_st_in_tab_pie_qry_rslt1, values='RegisteredUser', names='District', 
                                    title='RegisteredUser Analysis by District')

            # Customize the layout if needed
            pie_chart_figg.update_layout(
                title_font=dict(size=33), 
                title_font_color='#AD71EF',
                font=dict(size=14),  # Set the font size for labels
                height=700,  # Set the height of the plot
                width=800)            
                     
            # Display the pie chart
            st.plotly_chart(pie_chart_figg, use_container_width=True) 

            #Transaction count Analysis pie chart query
            cursor.execute(f"SELECT Districts, AppOpens FROM map_user WHERE States = '{st_ur_st}' AND Years = '{st_ur_yr}' AND Quarter = '{st_ur_qtr}';")
            in_ct_tab_pie_qry_rslt = cursor.fetchall()
            df_in_ct_tab_pie_qry_rslt = pd.DataFrame(np.array(in_ct_tab_pie_qry_rslt),
                                                     columns=['District', 'AppOpens'])
            df_in_ct_tab_pie_qry_rslt1 = df_in_ct_tab_pie_qry_rslt.set_index(
                pd.Index(range(1, len(df_in_ct_tab_pie_qry_rslt) + 1)))

            col4, col5 = st.columns(2)
            with col4:
                st.subheader(':violet[District via RegisteredUser]')
                st.dataframe(df_st_in_tab_pie_qry_rslt1)            
            with col5:
                st.subheader(':violet[District via AppOpens]')
                st.dataframe(df_in_ct_tab_pie_qry_rslt1)


            # Convert data types if necessary
            df_in_ct_tab_pie_qry_rslt1['AppOpens'] = df_in_ct_tab_pie_qry_rslt1['AppOpens'].astype(int)

            # Create the pie chart
            donot_chart_figg = px.bar(df_in_ct_tab_pie_qry_rslt1, y='AppOpens', x='District', 
                                    title='AppOpens Count Analysis by District')

            # Customize the layout if needed
            donot_chart_figg.update_layout(
                title_font=dict(size=33), 
                title_font_color='#AD71EF',
                font=dict(size=14),  # Set the font size for labels
                height=700,  # Set the height of the plot
                width=800)

            # Display the pie chart
            st.plotly_chart(donot_chart_figg, use_container_width=True)             


        #                  ------------------------------INSURANCE TAB FOR MAP--------------------------
        with tab5:
            col1, col2, col3 = st.columns(3)
            with col1:
                st_in_st = st.selectbox('**Select State**', (
                    'Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal'), key='st_in_st')
            with col2:
                st_in_yr = st.selectbox('**Select Year**', ('2020', '2021', '2022', '2023'), key='st_in_yr')
            with col3:
                if st_in_yr == '2020':
                    st_in_qtr = st.selectbox('**Select Quarter**', ('2', '3', '4'), key='st_in_qtr')
                else:    
                    st_in_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_in_qtr')

            #Transaction Analysis pie chart query
            cursor.execute(f"SELECT District, Transaction_amount FROM map_insurance WHERE States = '{st_in_st}' AND Years = '{st_in_yr}' AND Quarter = '{st_in_qtr}';")
            st_in_tab_pie_qry_rslt = cursor.fetchall()
            # Check if data is empty before creating DataFrame
 
            df_st_in_tab_pie_qry_rslt = pd.DataFrame(np.array(st_in_tab_pie_qry_rslt),
                                                    columns=['District', 'Insurance_amount'])
            df_st_in_tab_pie_qry_rslt1 = df_st_in_tab_pie_qry_rslt.set_index(
                pd.Index(range(1, len(df_st_in_tab_pie_qry_rslt) + 1)))


            # Convert data types if necessary
            df_st_in_tab_pie_qry_rslt1['Insurance_amount'] = df_st_in_tab_pie_qry_rslt1['Insurance_amount'].astype(float)

            # Create the pie chart
            pie_chart_figg = px.pie(df_st_in_tab_pie_qry_rslt1, values='Insurance_amount', names='District', 
                                    title='Insurance Analysis by District')

            # Customize the layout if needed
            pie_chart_figg.update_layout(
                title_font=dict(size=33), 
                title_font_color='#AD71EF',
                font=dict(size=14),  # Set the font size for labels
                height=700,  # Set the height of the plot
                width=800)            
                     
            # Display the pie chart
            st.plotly_chart(pie_chart_figg, use_container_width=True) 

            #Transaction count Analysis pie chart query
            cursor.execute(f"SELECT District, Transaction_count FROM map_insurance WHERE States = '{st_in_st}' AND Years = '{st_in_yr}' AND Quarter = '{st_in_qtr}';")
            in_ct_tab_pie_qry_rslt = cursor.fetchall()
            df_in_ct_tab_pie_qry_rslt = pd.DataFrame(np.array(in_ct_tab_pie_qry_rslt),
                                                     columns=['District', 'Insurance_count'])
            df_in_ct_tab_pie_qry_rslt1 = df_in_ct_tab_pie_qry_rslt.set_index(
                pd.Index(range(1, len(df_in_ct_tab_pie_qry_rslt) + 1)))

            col4, col5 = st.columns(2)
            with col4:
                st.subheader(':violet[District via Insurance amount]')
                st.dataframe(df_st_in_tab_pie_qry_rslt1)            
            with col5:
                st.subheader(':violet[District via Insurance count]')
                st.dataframe(df_in_ct_tab_pie_qry_rslt1)


            # Convert data types if necessary
            df_in_ct_tab_pie_qry_rslt1['Insurance_count'] = df_in_ct_tab_pie_qry_rslt1['Insurance_count'].astype(int)

            # Create the pie chart
            donot_chart_figg = px.bar(df_in_ct_tab_pie_qry_rslt1, y='Insurance_count', x='District', 
                                    title='Insurance Count Analysis by District')

            # Customize the layout if needed
            donot_chart_figg.update_layout(
                title_font=dict(size=33), 
                title_font_color='#AD71EF',
                font=dict(size=14),  # Set the font size for labels
                height=700,  # Set the height of the plot
                width=800)

            # Display the pie chart
            st.plotly_chart(donot_chart_figg, use_container_width=True)            

#--------------------------------------------------------TOP TAB---------------------------------------------------------------------------
    if select == "TOP":
        tab3 ,tab4, tab5 = st.tabs(["TRANSACTION","USER",'INSURANCE' ])

        #               --------------------------- TOP TRANSACTION ------------------------------------ 
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                tp_tr_yr = st.selectbox('**Select Year**', ('2020', '2021', '2022', '2023'), key='tp_tr_yr')
            with col2:
                if tp_tr_yr == '2020':
                    tp_tr_qtr = st.selectbox('**Select Quarter**', ('2', '3', '4'), key='tp_tr_qtr')
                else:                       
                    tp_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='tp_tr_qtr')

            cursor.execute(f"SELECT States, SUM(Transaction_amount) FROM top_transaction WHERE Years = '{tp_tr_yr}' AND Quarter = '{tp_tr_qtr}' GROUP BY States;")
            tp_tr_tab_qry_rslt = cursor.fetchall()
            df_tp_tr_tab_qry_rslt = pd.DataFrame(np.array(tp_tr_tab_qry_rslt), columns=['State', 'Transaction amount'])
            df_tp_tr_tab_qry_rslt1 = df_tp_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_tp_tr_tab_qry_rslt) + 1)))
    
             # GEO VISUALIZATION FOR USER

            # Drop a State column from df_in_us_tab_qry_rslt
            df_tp_tr_tab_qry_rslt.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['Transaction amount'] = df_tp_tr_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('State_tr_amt.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_tr_amt.csv')
            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='Transaction amount',
                color_continuous_scale='thermal', title='Transaction amount Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_use, use_container_width=True)

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(Transaction_count) FROM top_transaction WHERE Years = '{tp_tr_yr}' AND Quarter = '{tp_tr_qtr}' GROUP BY States;")
            tp_tr_tab_qry_rslt_b = cursor.fetchall()
            df_tp_tr_tab_qry_rslt_b= pd.DataFrame(np.array(tp_tr_tab_qry_rslt_b), columns=['State', 'Transaction count'])
            df_tp_tr_tab_qry_rslt1_b = df_tp_tr_tab_qry_rslt_b.set_index(pd.Index(range(1, len(df_tp_tr_tab_qry_rslt_b) + 1)))

            col3, col4 = st.columns(2)
            with col3:
                st.subheader(':violet[Transaction amount Analysis]')
                st.dataframe(df_tp_tr_tab_qry_rslt1)
            with col4:
                st.subheader(':violet[Transaction Count]')
                st.dataframe(df_tp_tr_tab_qry_rslt1_b)

            df_tp_tr_tab_qry_rslt1_b['State'] = df_tp_tr_tab_qry_rslt1_b['State'].astype(str)
            df_tp_tr_tab_qry_rslt1_b['Transaction count'] = df_tp_tr_tab_qry_rslt1_b['Transaction count'].astype(int)
            df_tp_tr_tab_qry_rslt1_b_fig = px.bar(df_tp_tr_tab_qry_rslt1_b, x='State', y='Transaction count', color='Transaction count',
                                                color_continuous_scale='thermal', title='Transaction count Analysis Chart',
                                                height=700, )
            df_tp_tr_tab_qry_rslt1_b_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_tp_tr_tab_qry_rslt1_b_fig, use_container_width=True) 

        #               --------------------------- TOP USER ------------------------------------
        with tab4:
            col1, col2, col3 = st.columns(3)
            with col1:
                st_ur_st = st.selectbox('**Select State**', (
                    'All','Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal'), key='st_ur_st')

            with col2:
                tp_ur_yr = st.selectbox('**Select Year**', ('2018','2019','2020', '2021', '2022', '2023' ), key='tp_ur_yr') 
            with col3:
                if tp_ur_yr == '2023':
                    tp_ur_qtr = st.selectbox('**Select Quarter**', ( '1','2', '3'), key='tp_ur_qtr')
                else:                       
                    tp_ur_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='tp_ur_qtr') 

            if st_ur_st == 'All':     

                cursor.execute(f"SELECT States, SUM(RegisteredUser) FROM top_user WHERE Years = '{tp_ur_yr}' AND Quarter = '{tp_ur_qtr}' GROUP BY States;")
                tp_ur_tab_qry_rslt = cursor.fetchall()
                df_tp_ur_tab_qry_rslt = pd.DataFrame(np.array(tp_ur_tab_qry_rslt), columns=['State', 'User count'])
                df_tp_ur_tab_qry_rslt1 = df_tp_ur_tab_qry_rslt.set_index(pd.Index(range(1, len(df_tp_ur_tab_qry_rslt) + 1)))
        
                # GEO VISUALIZATION FOR USER

                # Drop a State column from df_in_us_tab_qry_rslt
                df_tp_ur_tab_qry_rslt.drop(columns=['State'], inplace=True)
                # Clone the gio data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data2 = json.loads(response.content)
                # Extract state names and sort them in alphabetical order
                state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
                state_names_use.sort()
                # Create a DataFrame with the state names column
                df_state_names_use = pd.DataFrame({'State': state_names_use})
                # Combine the Gio State name with df_in_tr_tab_qry_rslt
                df_state_names_use['User count'] = df_tp_ur_tab_qry_rslt
                # convert dataframe to csv file
                df_state_names_use.to_csv('State_ur_ct.csv', index=False)
                # Read csv
                df_use = pd.read_csv('State_ur_ct.csv')
                # Geo plot
                fig_use = px.choropleth(
                    df_use,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM', locations='State', color='User count',
                    color_continuous_scale='thermal', title='User count Analysis')
                fig_use.update_geos(fitbounds="locations", visible=False)
                fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
                st.plotly_chart(fig_use, use_container_width=True)


                st.subheader(':violet[State via Total Users Analysis]')
                st.dataframe(df_tp_ur_tab_qry_rslt1)

            else: 
                col4, col5 = st.columns(2)
                with col4:  
                    cursor.execute(f"SELECT States, RegisteredUser, Pincodes FROM top_user WHERE States= '{st_ur_st}' AND Years = '{tp_ur_yr}' AND Quarter = '{tp_ur_qtr}';")
                    tp_ur_tab_qry_rslt = cursor.fetchall()
                    df_tp_ur_tab_qry_rslt = pd.DataFrame(np.array(tp_ur_tab_qry_rslt), columns=['State', 'User count', 'Pincodes'])
                    df_tp_ur_tab_qry_rslt1 = df_tp_ur_tab_qry_rslt.set_index(pd.Index(range(1, len(df_tp_ur_tab_qry_rslt) + 1))) 

                    st.subheader(':violet[User Dataframe Analysis]')
                    st.dataframe(df_tp_ur_tab_qry_rslt1)
                with col5:
                    cursor.execute(f"SELECT States, SUM(RegisteredUser) FROM top_user WHERE States= '{st_ur_st}' AND Years = '{tp_ur_yr}' AND Quarter = '{tp_ur_qtr}';")
                    tp_ur_tab_qry_rslt3 = cursor.fetchall()
                    df_tp_ur_tab_qry_rslt3= pd.DataFrame(np.array(tp_ur_tab_qry_rslt3), columns=['State', 'Total User count'])
                    df_tp_ur_tab_qry_rslt4 = df_tp_ur_tab_qry_rslt3.set_index(pd.Index(range(1, len(df_tp_ur_tab_qry_rslt3) + 1)))
                    st.subheader(':violet[Total User Dataframe]')
                    st.dataframe(df_tp_ur_tab_qry_rslt4)
        #               --------------------------- TOP INSURANCE ------------------------------------
        with tab5:
            col1, col2 = st.columns(2)
            with col1:
                tp_in_yr = st.selectbox('**Select Year**', ('2020', '2021', '2022', '2023'), key='tp_in_yr')
            with col2:
                if tp_in_yr == '2020':
                    tp_in_qtr = st.selectbox('**Select Quarter**', ('2', '3', '4'), key='tp_in_qtr')
                else:                       
                    tp_in_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='tp_in_qtr')

            cursor.execute(f"SELECT States, SUM(Transaction_amount) FROM top_insurance WHERE Years = '{tp_in_yr}' AND Quarter = '{tp_in_qtr}' GROUP BY States;")
            tp_in_tab_qry_rslt = cursor.fetchall()
            df_tp_in_tab_qry_rslt = pd.DataFrame(np.array(tp_in_tab_qry_rslt), columns=['State', 'Insurance amount'])
            df_tp_in_tab_qry_rslt1 = df_tp_in_tab_qry_rslt.set_index(pd.Index(range(1, len(df_tp_in_tab_qry_rslt) + 1)))
    
             # GEO VISUALIZATION FOR USER

            # Drop a State column from df_in_us_tab_qry_rslt
            df_tp_in_tab_qry_rslt.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['Insurance amount'] = df_tp_in_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('State_in_amt.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_in_amt.csv')
            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM', locations='State', color='Insurance amount',
                color_continuous_scale='thermal', title='Insurance amount Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
            st.plotly_chart(fig_use, use_container_width=True)

            # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(Transaction_count) FROM top_insurance WHERE Years = '{tp_in_yr}' AND Quarter = '{tp_in_qtr}' GROUP BY States;")
            tp_in_tab_qry_rslt_b = cursor.fetchall()
            df_tp_in_tab_qry_rslt_b= pd.DataFrame(np.array(tp_in_tab_qry_rslt_b), columns=['State', 'Insurance count'])
            df_tp_in_tab_qry_rslt1_b = df_tp_in_tab_qry_rslt_b.set_index(pd.Index(range(1, len(df_tp_in_tab_qry_rslt_b) + 1)))

            col3, col4 = st.columns(2)
            with col3:
                st.subheader(':violet[Transaction amount Analysis]')
                st.dataframe(df_tp_in_tab_qry_rslt1)
            with col4:
                st.subheader(':violet[Transaction Count]')
                st.dataframe(df_tp_in_tab_qry_rslt1_b)

            df_tp_in_tab_qry_rslt1_b['State'] = df_tp_in_tab_qry_rslt1_b['State'].astype(str)
            df_tp_in_tab_qry_rslt1_b['Insurance count'] = df_tp_in_tab_qry_rslt1_b['Insurance count'].astype(int)
            df_tp_in_tab_qry_rslt1_b_fig = px.bar(df_tp_in_tab_qry_rslt1_b, x='State', y='Insurance count', color='Insurance count',
                                                color_continuous_scale='thermal', title='Insurance count Analysis Chart',
                                                height=700, )
            df_tp_in_tab_qry_rslt1_b_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_tp_in_tab_qry_rslt1_b_fig, use_container_width=True)

#----------------------------------------------------- Insights TAB---------------------------------------------------------------------------
if selected == "Insights":
    st.title(':violet[BASIC INSIGHTS]')
    st.subheader("The basic insights are derived from the Analysis of the Phonepe Pulse data. It provides a clear idea about the analysed data.")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "Least 10 states based on year and amount of transaction",
               "Top 10 Districts based on the Transaction Amount",
               "Least 10 Districts based on the Transaction Amount",
               "Top 10 Districts based on the Transaction count",
               "Least 10 Districts based on the Transaction count",
               "Top Transaction types based on the Transaction Amount",
               "Top 10 Mobile Brands based on the User count of transaction",
               "Top 5 Brands based on  count of transaction",
               "Least 5 Brands based on count of transaction"]
    select = st.selectbox(":violet[Select the option]",options)

    #1
    if select == "Top 10 states based on year and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT States,Years, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY States,Years ORDER BY Total_Transaction_Amount DESC LIMIT 10");

        data = cursor.fetchall()
        columns = ['States', 'Year', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        df['Year'] = df['Year'].astype(str)    
        df['Year'] = df['Year'].str.replace(',', '')

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 states based on amount of transaction")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df["States"], df["Transaction_amount"], color='blue')

            # Set labels and title
            plt.xlabel('States')
            plt.ylabel('Transaction Amount')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)

    #2
    elif select == "Least 10 states based on year and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT States,Years, SUM(Transaction_amount) as Total FROM top_transaction GROUP BY States, Years ORDER BY Total ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'Year', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))
            # Remove commas from the 'Year' column
        df['Year'] = df['Year'].astype(str)    
        df['Year'] = df['Year'].str.replace(',', '')

        # Convert 'Year' column to integer type
 
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 states based on amount of transaction")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df["States"], df["Transaction_amount"], color='blue')

            # Set labels and title
            plt.xlabel('States')
            plt.ylabel('Transaction Amount')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)



    #3
    elif select == "Top 10 Districts based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT States ,District,SUM(Transaction_Amount) AS Total FROM map_transaction GROUP BY States ,District ORDER BY Total DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on Transaction Amount")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df["District"], df["Transaction_Amount"], color='red')

            # Set labels and title
            plt.xlabel('District')
            plt.ylabel('Transaction Amount')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)

    # 4
    elif select == "Least 10 Districts based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT States,District,SUM(Transaction_amount) AS Total FROM map_transaction GROUP BY States, District ORDER BY Total ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on Transaction Amount")
                        # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df["States"], df["Transaction_amount"], color='blue')

            # Set labels and title
            plt.xlabel('States')
            plt.ylabel('Transaction Amount')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)


    # 5
    elif select == "Top 10 Districts based on the Transaction count":
        cursor.execute(
            "SELECT DISTINCT States,District,SUM(Transaction_count) AS Counts FROM map_transaction GROUP BY States ,District ORDER BY Counts DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on Transaction Count")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df["States"], df["Transaction_Count"], color='blue')

            # Set labels and title
            plt.xlabel('States')
            plt.ylabel('Transaction_Count')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)


    # 6
    elif select == "Least 10 Districts based on the Transaction count":
        cursor.execute(
            "SELECT DISTINCT States ,District,SUM(Transaction_count) AS Counts FROM map_transaction GROUP BY States ,District ORDER BY Counts ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on the Transaction Count")
                        # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df["States"], df["Transaction_Count"], color='blue')

            # Set labels and title
            plt.xlabel('States')
            plt.ylabel('Transaction_Count')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)


    #7
    elif select == "Top Transaction types based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5");
        data = cursor.fetchall()
        columns = ['Transaction_type', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top Transaction Types based on the Transaction Amount")
                        # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df['Transaction_type'], df["Transaction_amount"], color='blue')

            # Set labels and title
            plt.xlabel('Transaction_type')
            plt.ylabel('Transaction Amount')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)


    #8
    elif select == "Top 10 Mobile Brands based on the User count of transaction":
        cursor.execute(
            "SELECT DISTINCT Brands,SUM(Transaction_Count) as Total FROM aggregated_user GROUP BY Brands ORDER BY Total DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['Brands', 'User_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Mobile Brands based on User count of transaction")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.bar(df['Brands'], df['User_Count'], color='blue')

            # Set labels and title
            plt.xlabel('Brands')
            plt.ylabel('User_Count')

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)

            # Display the plot
            st.pyplot(plt)
   

    #9
    elif select == "Top 5 Brands based on  count of transaction":
        cursor.execute(
            "SELECT Brands, SUM(Transaction_count) as Total FROM aggregated_user GROUP BY Brands  ORDER BY Total DESC LIMIT 5;");
        data = cursor.fetchall()
        columns = ['Brands', 'Transaction_count']
        df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 5 Brands based on count of transaction")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.pie( df["Transaction_count"], labels = df["Brands"],  autopct='%1.1f%%', startangle=140)

            # Display the plot
            st.pyplot(plt)

    #10
    elif select == "Least 5 Brands based on count of transaction":
        cursor.execute(
            "SELECT Brands, SUM(Transaction_count) as Total FROM aggregated_user GROUP BY Brands  ORDER BY Total ASC LIMIT 5;");
        data = cursor.fetchall()
        columns = ['Brands', 'Transaction_count']
        df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 5 Brands based on count of transaction")
            # Create a bar chart using Matplotlib
            plt.figure(figsize=(10, 6))
            plt.pie( df["Transaction_count"], labels = df["Brands"],  autopct='%1.1f%%', startangle=140)

            # Display the plot
            st.pyplot(plt)            


#------------------------------------------------------Contact TAB---------------------------------------------------------------------------
if selected == "Contact":
    col1, col2 = st.columns(2)  
    col2.image(Image.open(r'C:\Users\gowth\Downloads\project_phonepe\files\gowtham.JPG'), width=600)
    with col1:
        st.markdown("# :violet[Done by] : GOWTHAM E") 
        st.markdown("## :An Aspiring DATA-SCIENTIST..!")
        st.markdown("Gmail: gowthame82000@gmail.com")
        st.markdown("[Inspired from](https://www.phonepe.com/pulse/)")
        st.markdown("[Githublink](https://github.com/Gowthame123)")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/gowthamesakki/)") 
st.write("---")        










