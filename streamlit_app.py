# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

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

#session = get_active_session()
cnx = st.connection('snowflake')
session = cnx.session()
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
         st.subheader(fruit_chosen + ' Nutrition')
         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
         st.write(smoothiefroot_response.status_code)
         if smoothiefroot_response.status_code == 200:
           sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
           st.write('200 if then')
         if smoothiefroot_response.status_code != 200:
           st.write('not 200 if then')
           search_name_df = (
                    session.table("smoothies.public.fruit_options")
                    .filter(col("FRUIT_NAME") == fruit_chosen)
                    .select(col("SEARCH_ON"))  )
           search_name_result = search_name_df.collect()
           alternate_search_term = search_name_result[0][0]
           st.write("https://my.smoothiefroot.com/api/fruit/" + alternate_search_term)
           smoothiefrootAlter_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + alternate_search_term)
           sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
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


#st.text(smoothiefroot_response.json())

