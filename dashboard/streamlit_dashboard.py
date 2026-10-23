import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings



st.set_page_config(page_title="Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")
st.title(":chart_with_upwards_trend: covid 19")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if f1 is not None:

    dataset = pd.read_csv(f1, encoding= "ISO-8859-1")
# else:
#      dataset = pd.read_csv('train.csv', encoding= "ISO-8859-1")


    col1, col2 = st.columns((2))
    
    
    dataset = dataset[(dataset["reactivity"] >= 0) & (dataset["reactivity"] <= 1)].copy()
    
    
    page = st.sidebar.selectbox("Select a Page", ["Page One", "Page Two"])
    st.sidebar.title("Column Selector")
    column_names = dataset.select_dtypes(include='number').columns.tolist()
    selected_columns = st.sidebar.multiselect("Select Y-axis Columns:", column_names)
    selected_to_box_columns = st.sidebar.multiselect("Select Columns to boxplot:", column_names)
    x_column = st.sidebar.selectbox("Select X-axis Column:", ["sequence",'predicted_loop_type'])
    
    
    page_one_key = "page_one_key"
    page_two_key = "page_two_key"
    
    
    if page == "Page One":
        st.write(dataset.describe())
        if selected_columns :
            selected_column = selected_columns[0] 
            dataset = dataset[(dataset[selected_column] >= 0) & (dataset[selected_column] <= 1)].copy()
            sequence_df = dataset.groupby(by=["sequence"], as_index=False)[selected_column].mean()
            with col1:
                st.subheader(f"{selected_column} V sequence")
                fig = px.bar(sequence_df, x="sequence", y=selected_column, text=[f'%{{:,.2f}}'.format(x) for x in sequence_df[selected_column]],
                     template="seaborn")
                st.plotly_chart(fig, use_container_width=True, height=200)
    
            sequence_df = dataset.groupby(by = ["sequence"], as_index = False)["reactivity"].mean()
            with col2:
                st.subheader("sequence")
                fig = px.pie(sequence_df, values = "reactivity", names = "sequence", hole = 0.5)
                fig.update_traces(text = sequence_df["sequence"],textinfo="percent+label")
                st.plotly_chart(fig,use_container_width=True)
    
    
        cl1, cl2 = st.columns((2))
    
        if selected_columns and x_column:
            selected_column = selected_columns[0]  
            dataset = dataset[(dataset[selected_column] >= 0) & (dataset[selected_column] <= 1)].copy()
        
        
            predicted_df = dataset.groupby(by=["predicted_loop_type"], as_index=False)[selected_column].mean()
        
            with cl1:
                st.subheader(f"{selected_column} V Predicted Loop Types")
                fig = px.bar(predicted_df, x="predicted_loop_type", y=selected_column, text=[f'%{{:,.2f}}'.format(x) for x in predicted_df[selected_column]],
                     template="seaborn")
                st.plotly_chart(fig, use_container_width=True, height=200)
         
            with cl2:
                st.subheader("Distribution of Predicted Loop Types")
                pie_fig = px.pie(predicted_df, values=selected_column, names="predicted_loop_type", hole=0.5)
                pie_fig.update_traces(textinfo="percent+label")
                st.plotly_chart(pie_fig, use_container_width=True)
    
    
    
    
    
    elif page == "Page Two":
        if selected_to_box_columns:
            selected_box_column = selected_to_box_columns
            with st.container():
                st.subheader(f"Box Plot of {selected_box_column}")
                fig = px.box(dataset, y=selected_box_column, template="seaborn")
                st.plotly_chart(fig, use_container_width=True) 
    
    
        clo1, clo2 = st.columns((2))
        with clo1:
            if selected_columns:
                selected_column = selected_columns
                if len(selected_columns) == 4:
                    y_column_1, y_column_2,y_column_3, y_column_4 = selected_columns[0], selected_columns[1],selected_columns[2], selected_columns[3]
    
                    line = dataset.groupby(by='sequence',as_index=False)[[y_column_1, y_column_2,y_column_3, y_column_4]].mean()
                    
                    fig = px.area(line, x='sequence', y=[y_column_1, y_column_2, y_column_3, y_column_4])
                    fig.update_layout(title='Area Plot', xaxis_title='sequence', yaxis_title=selected_column[0])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    
                    line = dataset.groupby(by='sequence',as_index=False)[[selected_columns[0]]].mean()
                    fig = px.line(line, x='sequence', y=selected_columns[0])
                    fig.update_layout(title='Line Graph', xaxis_title='sequence', yaxis_title=selected_column[0])
                    st.plotly_chart(fig, use_container_width=True)            
        with clo2:
            if selected_columns:
                selected_column = selected_columns
                if len(selected_columns) == 4:
                    y_column_1, y_column_2,y_column_3, y_column_4 = selected_columns[0], selected_columns[1],selected_columns[2], selected_columns[3]
    
                    line = dataset.groupby(by='predicted_loop_type',as_index=False)[[y_column_1, y_column_2,y_column_3, y_column_4]].mean()
                    fig = px.line(line, x='predicted_loop_type', y=[y_column_1, y_column_2,y_column_3, y_column_4])
                    fig.update_layout(title='Line Graph', xaxis_title='predicted_loop_type', yaxis_title=selected_column[0])
                    st.plotly_chart(fig, use_container_width=True)    
    
                else:
                    
                    line = dataset.groupby(by='predicted_loop_type',as_index=False)[[selected_columns[0]]].mean()
                    fig = px.line(line, x='predicted_loop_type', y=selected_columns[0])
                    fig.update_layout(title='Line Graph', xaxis_title='predicted_loop_type', yaxis_title=selected_column[0])
                    st.plotly_chart(fig, use_container_width=True)  
            
        with st.container():
            data=dataset.select_dtypes(include='number')
            st.subheader(f"Heat map for dataset")
            fig, ax = plt.subplots(figsize=(10, 8))
            heatmap = sns.heatmap(data.corr(), cmap="YlGnBu", annot=True)
            st.pyplot(fig)









