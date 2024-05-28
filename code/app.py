import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, value

def create_data_entry():
    st.sidebar.header('Supply Nodes')
    factories = st.sidebar.text_area("Enter factories, separated by commas").split(',')

    st.sidebar.header('Supply Quantities')
    supply = {factory: st.sidebar.number_input(f"Supply for {factory}", min_value=0) for factory in factories}

    st.sidebar.header('Demand Nodes')
    projects = st.sidebar.text_area("Enter projects, separated by commas").split(',')

    st.sidebar.header('Demand Quantities')
    demand = {project: st.sidebar.number_input(f"Demand for {project}", min_value=0) for project in projects}

    st.sidebar.header('Intermediate Nodes')
    warehouses = st.sidebar.text_area("Enter warehouses, separated by commas").split(',')

    st.sidebar.header('Costs from Factories to Warehouses')
    costs_1 = [[st.number_input(f"Cost from {factory} to {warehouse}", min_value=0.0) for warehouse in warehouses] for factory in factories]

    st.sidebar.header('Costs from Warehouses to Projects')
    costs_2 = [[st.number_input(f"Cost from {warehouse} to {project}", min_value=0.0) for project in projects] for warehouse in warehouses]

    return factories, supply, projects, demand, warehouses, costs_1, costs_2

def main():
    st.title('Waste Management Optimization Model')
    
    factories, supply, projects, demand, warehouses, costs_1, costs_2 = create_data_entry()
    
    if st.button('Show Data'):
        st.write("Factories:", factories)
        st.write("Supply:", supply)
        st.write("Projects:", projects)
        st.write("Demand:", demand)
        st.write("Warehouses:", warehouses)
        st.write("Costs from Factories to Warehouses:", pd.DataFrame(costs_1, columns=warehouses, index=factories))
        st.write("Costs from Warehouses to Projects:", pd.DataFrame(costs_2, columns=projects, index=warehouses))

if __name__ == '__main__':
    main()
