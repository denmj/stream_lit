import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import streamlit as st


st.write("""
    # Streamlit App Framework
    by *Denis M*

""")

electric_data = pd.read_csv(
  "C://Users//denis//Desktop//st_test_lit//stream_lit//Electric_Production.csv").rename(columns={
                                                                                        'IPG2211A2N': 'Value'})


# df = pd.DataFrame({
#
#   'date': ['10/1/2019','10/2/2019', '10/3/2019', '10/4/2019'],
#   'second column': [10, 20, 30, 40]
# })

np.random.seed(42)
source = pd.DataFrame(np.cumsum(np.random.randn(100, 3), 0).round(2),
                    columns=['A', 'B', 'C'], index=pd.RangeIndex(100, name='x'))

source = source.reset_index().melt('x', var_name='category', value_name='y')

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['DATE'], empty='none')

# The basic line
line = alt.Chart(electric_data).mark_line(interpolate='basis').encode(
    x='DATE:T',
    y='Value:Q'
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = alt.Chart(electric_data).mark_point().encode(
    x='DATE:T',
    opacity=alt.value(0),
).add_selection(
    nearest
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'Value:Q', alt.value(' '))
)

# Draw a rule at the location of the selection
rules = alt.Chart(electric_data).mark_rule(color='gray').encode(
    x='DATE:T',
).transform_filter(
    nearest
)

# Put the five layers into a chart and bind the data
chart = alt.layer(
    line, selectors, points, rules, text
).properties(
    width=600, height=300
)

st.altair_chart(chart)

# electric_data.rename(columns={'DATE':'index'}).set_index('index')