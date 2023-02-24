import streamlit
import pandas
import snowflake.connector
import requests

from urllib.error import URLError


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

# Let's put a pick list here so they can pick the fruit they want to include 

# Display the table on the page.


############################################
#create the repeatable code block
def get_fruitvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice) 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
# new section to display fruityvice api response    
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("please select a fruit to get informaiton.")
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
  
############################################
    

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
        with  my_cnx.cursor() as my_cur:
                my_cur.execute("select * from fruit_load_list")
                return my_cur.fetchall()
            
if streamlit.button('get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


streamlit.stop()
    

fruit_choice_add = streamlit.text_input('Waht fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")




