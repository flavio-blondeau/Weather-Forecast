import streamlit as st
import plotly.express as px
from backend import get_data

# Add widgets
st.title("Weather Forecast for the next days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")


if place:
    # Get temperature/sky data
    try:
        data = get_data(place, days)

        # Create temperature plot
        if option == 'Temperature':
            temperatures = [d['main']['temp'] - 273.15 for d in data]
            dates = [d['dt_txt'] for d in data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == 'Sky':
            sky_condition = [d['weather'][0]['main'] for d in data]
            images = {"Clear": "images/clear.png",
                      "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png",
                      "Snow": "images/snow.png"}
            image_paths = [images[condition] for condition in sky_condition]
            st.image(image_paths, width=120)
    except KeyError:
        st.write("This place does not exist! "
                 "Make sure you have written the name correctly with capital letter.")

