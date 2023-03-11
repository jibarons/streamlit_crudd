# https://blog.streamlit.io/how-to-build-a-real-time-live-dashboard-with-streamlit/
# deploy: https://share.streamlit.io/
# https://jibarons-ict-survey-app-zy2akr.streamlit.app/?embedded=true

import getpass
from datetime import date
#from sqlalchemy.engine import result, URL
import sqlalchemy as sa
#from sqlalchemy import create_engine, MetaData, text, Date, update 
import psycopg2
import os
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # data web app development


st.set_page_config(
    page_title="ICT Satisfaction Survey",
    #page_icon="✅",
    layout="wide",
)

# @st.cache prevents the streamlit app from executing redundant processes
# repeatedly that are expensive such as database connections or reading input


pwd = st.text_input("Enter server password", type="password")
#pwd = getpass.getpass()

if pwd:

  conn = sa.engine.URL.create(
      drivername="postgresql+psycopg2",
      username="postgres",
      password=pwd,
      host="localhost",
      database="data_tech",
  )

  @st.cache_resource
  def get_conn():
      engine = sa.create_engine(conn)
      return engine

  engine = get_conn() 
  engine = sa.create_engine(conn)
  meta = sa.MetaData(bind=engine)
  sa.MetaData.reflect(meta)

  @st.cache_data
  def get_data(table)-> pd.DataFrame:
      return pd.read_sql_query('SELECT * FROM public.' + table, con=engine)

  def add_entry():
      df_oppo_entry.to_sql('opportunity',  engine, if_exists='append', index = False)    

  def update_entry(table, data_dict):
      tbl_oppo = sa.meta.tables[table]
      # update
      u = sa.update(tbl_oppo)
      u = u.values(data_dict)
      u = u.where(tbl_oppo.c.init_name == initiative_filter)
      engine.execute(u)
      # write the SQL query inside the
      # text() block to fetch all records
      sql = text('SELECT * from ' + table)
      # Fetch all the records
      result = engine.execute(sql).fetchall()

  def pivot_data(df): 
      df_wide = df.pivot(index=['submit_date', 'submit_name', 'submit_email',
        'init_id', 'init_uuid', 'init_formid'], columns='fields', values = 'values')
      df_wide = df_wide.reset_index()
      df_wide.columns.name = None
      return(df_wide)

  df = get_data('initiatives')
  df_wide = pivot_data(df)

  # df.info()
  df_oppo = get_data('opportunity')



  df_wide_id = df_wide['init_name']


  # dashboard title
  st.title("Data-Tech SOMETHING something")

  # top-level filters
  # country_filter = st.selectbox("Select Country", pd.unique(df_wide["country"]))
  initiative_filter = st.selectbox("Select Inititative", pd.unique(df_wide["init_name"]))

  st.write("You entered: ", initiative_filter)

  # dataframe filter
  idx = df_wide.index[df_wide["init_name"] == initiative_filter]
  df_wide = df_wide.loc[idx]


  # creating a single-element container
  placeholder = st.empty()
  with placeholder.container():

    tab1, tab2, tab3 = st.tabs(["Assessment", "Initiative Data", 'Opportunity Data'])
    
    with tab1:
      # Store the initial value of widgets in session state
      if "visibility" not in st.session_state:
          st.session_state.visibility = "visible"
          st.session_state.disabled = False
      # create two columns
      raw, input = st.columns(2) # for more than 1 metric
      # raw displays the initiative as provided by the initiative fp
      with raw:
        st.header("Initiative brief")
        st.write(df_wide["problem"])
        st.write(df_wide["overview"])

      with input:
          st.header("Opportunity assessment")

          st.write(len(df_oppo)-1)

          st.write("Outside the form")

          badd_entry = st.button('Add entry')

          with st.form("my_form"):
              st.write("Inside the form")
              team_feed = st.text_area(
                  "Team's feedback and overall comment",
                  label_visibility=st.session_state.visibility,
                  disabled=st.session_state.disabled
                  #placeholder=st.session_state.placeholder,
              )
              score = st.number_input(
                  'Score',
                  value=0,
                  label_visibility=st.session_state.visibility,
                  disabled=st.session_state.disabled
              )

              # Every form must have a submit button.
              submitted = st.form_submit_button("Submit")

              # Add assessment inputs to table
              # Create Opportunity data frame wfor stora of input values
              today = date.today()
              oppo_entry = {
                  'oppo_date': today.isoformat(),
                  'init_name': initiative_filter,
                  'oppo_feed': team_feed,
                  'init_id': df_wide['init_id'][0],
                  'init_uuid': df_wide['init_uuid'][0],
                  'init_formid': df_wide['init_formid'][0]
              }
              

              if submitted:
                  if any(initiative_filter == df_oppo['init_name']):
                    update_entry('opportunity', oppo_entry)
                    df_oppo = get_data('opportunity')
                    st.write("Entry updated")

                  else:
                    df_oppo_entry = pd.DataFrame(oppo_entry,  index=[0])
                    add_entry()
                    df_oppo = get_data('opportunity')
                    st.write("Entry added")

          st.write("Outside the form")
          st.write(len(df_oppo)-1)

          # # Enter opportunity assessment
          # team_feed = st.text_area(
          #     "Team's feedback and overall comment",
          #     label_visibility=st.session_state.visibility,
          #     disabled=st.session_state.disabled
          #     #placeholder=st.session_state.placeholder,
          # )

          # score = st.number_input(
          #     'Score',
          #     label_visibility=st.session_state.visibility,
          #     disabled=st.session_state.disabled
          # )

          # # Add assessment inputs to table
          # df_oppo['oppo_feed'] = team_feed
          # #df_oppo['score'] = score
          
          # if badd_entry:
          #   add_entry()



          # if team_feed:
          #     st.write("You entered: ", team_feed)

    with tab2:
      st.markdown("### Detailed Data View")
      st.dataframe(df_wide)
      # time.sleep(1)

    with tab3:
      st.markdown("### Detailed Data View")
      st.dataframe(df_oppo)
      # time.sleep(1)


    # runin cmd `streamlit run app.py`