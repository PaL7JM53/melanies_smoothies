# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your app :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

#option = st.selectbox(
#    "favorite fruit?",
#    ("apple", "banana", "grape"),
#)

#st.write("your fruit:", option)

name_on_order = st.text_input('Name on Smoothie')
st.write('the name on your smoothie',name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")
#st.dataframe(data=my_dataframe, use_container_width=True)

# 2. Select the desired column(s)
# Example: Selecting FRUIT_NAME and FRUIT_ID
selected_dataframe = my_dataframe.select(
    col("FRUIT_NAME")
)

# 3. Display the result
#st.dataframe(data=selected_dataframe, use_container_width=True)

ingredients_list = st.multiselect("choose up to 5:",selected_dataframe,max_selections = 5)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
         ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('submit order')
    if time_to_insert:
    #if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")
