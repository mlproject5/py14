import requests
import geocoder
import streamlit as st

st.set_page_config(page_title='PrayerTime', page_icon='pt.png', layout="centered", initial_sidebar_state="auto",
                   menu_items=None)


hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown(
    "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Prayer Times</h1></center>",
    unsafe_allow_html=True)

st.markdown(
    "<style>.stButton>button {margin: 0 auto; display: block;}</style>",
    unsafe_allow_html=True
)

location = st.empty()
location_button = st.button("Get Location")

if location_button:
    location.info("Locating...")
    g = geocoder.ip("me")
    if g.latlng:
        latitude, longitude = g.latlng
        location.success("Location found!")
    else:
        location.warning("Unable to retrieve location. Please enter the country and city manually.")

if "latitude" in locals() and "longitude" in locals():
    url = "https://api.aladhan.com/v1/calendarByCity"
    g = geocoder.osm([latitude, longitude], method='reverse')
    city = g.city
    country = g.country
    state = g.state
    postal_code = g.postal
    district = g.county

    querystring = {"city": city, "country": country, "method": "2"}

    headers = {
        "X-RapidAPI-Key": "7d64960abcmsh8aafaa658e604d1p18479djsn64c7151fa9b2",
        "X-RapidAPI-Host": "aladhan.p.rapidapi.com"
    }

    with st.spinner("Fetching prayer times..."):
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

    if "code" in data and data["code"] == 200:
        prayer_times = data["data"][0]["timings"]
        fajr = prayer_times["Fajr"]
        dhuhr = prayer_times["Dhuhr"]
        asr = prayer_times["Asr"]
        maghrib = prayer_times["Maghrib"]
        isha = prayer_times["Isha"]

        timings = data["data"][0]["timings"]
        sunrise = timings["Sunrise"]
        sunset = timings["Sunset"]

        centered_section = """
            <div style="text-align: center;">
                <p>Fajr: {fajr}</p>
                <p>Dhuhr: {dhuhr}</p>
                <p>Asr: {asr}</p>
                <p>Maghrib: {maghrib}</p>
                <p>Isha: {isha}</p>
                <p>Sunrise: {sunrise}</p>
                <p>Sunset: {sunset}</p>
            </div>
        """

        st.markdown(centered_section.format(
            fajr=fajr,
            dhuhr=dhuhr,
            asr=asr,
            maghrib=maghrib,
            isha=isha,
            sunrise=sunrise,
            sunset=sunset
        ), unsafe_allow_html=True)

        location_info = f"{district}, {city}, {state}, {postal_code}, {country}"
        st.markdown("<h3 style='text-align: center; position: fixed; bottom: 0; left: 0; right: 0; font-size: "
                    "medium;'>{}</h3>".format(location_info), unsafe_allow_html=True)

    else:
        st.write("Prayer times data not available.")

