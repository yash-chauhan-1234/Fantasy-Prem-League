import streamlit as st
import script
import numpy as np
import pandas as pd

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked=False

def callback():
    st.session_state.button_clicked=True

st.set_page_config(layout="wide")


DATA='D:\College\sem 5\AI\project\data'
st.title('Fantasy Premiere League')

week=st.selectbox("Week", ["Week 1","Week 2","Week 3","Week 4"])
team=st.selectbox("Number of players", ["All 15 players", "Only first 11"])


if st.button("Submit", on_click=callback) or st.session_state.button_clicked:

    wk=week.split()
    wk=int(wk[1])-1
    # defence, mid, forw=5,5,3
    optimisation_df, df=script.load_data(wk, DATA)
        

    try:
        actual_df, total_cost, total_points=script.knapsack(script.get_constraints(optimisation_df))

        if team=="All 15 players":
            st.write('Actual Team')

            st.dataframe(actual_df)
            st.text(f"Total Cost: {total_cost}")
            st.text(f"Total Points: {total_points}")


        else:
            with st.form("Formation Form"):
                st.write("Choose your formation")
                a=st.number_input("Enter Number of defenders", step=1, max_value=5, min_value=3)
                b=st.number_input("Enter Number of midfielders", step=1, max_value=5, min_value=3)
                c=st.number_input("Enter Number of attackers", step=1, max_value=3, min_value=1)
                # d=st.number_input("Enter Budget", step=1, min_value=80, max_value=100)
                
                if st.form_submit_button("Submit"):
                    
                    if a+b+c==10:
                        st.write('Actual Team')

                        df=script.get_df(actual_df, a, b, c)
                        st.dataframe(df)

                        st.text(f"Total Cost: {sum(df['Cost'])}")
                        st.text(f"Total Points: {sum(df['Points'])}")


                    else:
                        st.warning("There should be total 11 players")
                        st.stop()

    except:
        next_week=st.checkbox('Predict Next Week\'s Team')
        if next_week:
            rfr=script.RandomF(df)
            rfr.model_train()
            preds=np.round(rfr.predict(train=True))

            df["Points"]=preds
            predicted, total_cost_preds, total_points_preds=script.knapsack(script.get_constraints(df[["Name", "Team", "Position", "Cost", "Points"]]))
        
            st.write('Predicted Team')
            predicted.drop(['Points', 'Cost'], axis=1, inplace=True)
            st.dataframe(predicted)
        

            





