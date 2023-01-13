import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner!!')

streamlit.header('🥣Breakfast Menu')
streamlit.text('🥗Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fuits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.

streamlit.dataframe(my_fruit_list)
streamlit.header('🍌🥭 You select: 🥝🍇')

streamlit.dataframe(fuits_to_show)

def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())   
    return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  


def get_sf_fruit_list(v_cur):
    v_cur.execute("select * from fruit_load_list")
    return v_cur.fetchall()

def add_to_sf_fruit_list(v_cur, v_new_val):
    v_cur.execute("insert into fruit_load_list values ('"+v_new_val+"')")
    return "Thanks for adding " + v_new_val

if streamlit.button('Get Fruit Load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    streamlit.text(add_to_sf_fruit_list(my_cur, 'Carry'))
    streamlit.dataframe(get_sf_fruit_list(my_cur))
    
    


  
streamlit.stop()


my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

streamlit.header("!!Snowflake data:")
#my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("My fruit load list containts:")
streamlit.dataframe(my_data_row)


add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('From streamlit')")
