import streamlit as st
from src.prediction import predict_rain
from src.weather_api import get_weather_data

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Rain Prediction System",
    page_icon="🌧️",
    layout="centered"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.metric-card {
    background: #f7f7f5;
    border-radius: 8px;
    padding: 14px 16px;
}
.metric-label {
    font-size: 12px;
    color: #888;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 20px;
    font-weight: 500;
}
.metric-unit {
    font-size: 13px;
    font-weight: 400;
    color: #888;
}
.result-box {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    border-radius: 8px;
    margin-top: 8px;
}
.location-badge {
    display: inline-block;
    background: #f7f7f5;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 13px;
    color: #666;
}
.step-bar {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 20px;
}
.step-dot {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 600;
}
.step-line {
    flex: 1;
    height: 1px;
    background: #e0e0e0;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE
# =========================================

st.title("🌧️ Rain Prediction System")
st.write("Predict whether it will rain tomorrow using Machine Learning and Live Weather Data.")

# =========================================
# SIDEBAR
# =========================================

mode = st.sidebar.selectbox(
    "Choose Prediction Mode",
    ["Manual Prediction", "Live Weather Prediction"]
)

# =========================================
# MANUAL PREDICTION
# =========================================

if mode == "Manual Prediction":

    st.header("Manual Weather Input")

    col1, col2 = st.columns(2)

    with col1:
        MinTemp = st.number_input("Min Temperature", min_value=-10.0, max_value=50.0, value=20.0, step=0.1)
        Pressure9am = st.number_input("Pressure at 9am", value=1010.0)
        Temp9am = st.number_input("Temp at 9am", min_value=-10.0, max_value=50.0, value=22.0, step=0.1)
        Humidity9am = st.slider("Humidity at 9am", min_value=0.0, max_value=100.0, value=60.0)
        WindSpeed9am = st.slider("Wind Speed at 9am", min_value=0, max_value=150, value=10)

    with col2:
        MaxTemp = st.number_input("Max Temperature", min_value=-10.0, max_value=50.0, value=30.0, step=0.1)
        Pressure3pm = st.number_input("Pressure at 3pm", value=1008.0)
        Temp3pm = st.number_input("Temp at 3pm", min_value=-10.0, max_value=50.0, value=28.0, step=0.1)
        Humidity3pm = st.slider("Humidity at 3pm", min_value=0.0, max_value=100.0, value=65.0)
        WindSpeed3pm = st.slider("Wind Speed at 3pm", min_value=0, max_value=150, value=12)

    RainToday = st.selectbox(
        "Did it rain today?",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    if st.button("Predict Rain"):
        input_data = [
            MinTemp, MaxTemp, Humidity9am, Humidity3pm,
            Pressure9am, Pressure3pm, Temp9am, Temp3pm,
            WindSpeed9am, WindSpeed3pm, RainToday
        ]
        result = predict_rain(input_data)
        st.subheader("Prediction Result")
        if result == 1:
            st.error("🌧️ It will RAIN tomorrow")
        else:
            st.success("☀️ No rain tomorrow")

# =========================================
# LIVE WEATHER PREDICTION
# =========================================

else:
    st.header("🌍 Live Weather Prediction")

    # ── Init session state ──────────────────────────────────────────
    if "lw_step" not in st.session_state:
        st.session_state["lw_step"] = 1
    if "lw_matched_states" not in st.session_state:
        st.session_state["lw_matched_states"] = []
    if "lw_city" not in st.session_state:
        st.session_state["lw_city"] = ""
    if "lw_country" not in st.session_state:
        st.session_state["lw_country"] = "IN"
    if "lw_weather" not in st.session_state:
        st.session_state["lw_weather"] = None

    step = st.session_state["lw_step"]

    # ── Step progress bar ───────────────────────────────────────────
    def step_color(n):
        if n < step:
            return "background:#22c55e; color:#fff;"
        elif n == step:
            return "background:#111; color:#fff;"
        else:
            return "background:#f0f0f0; color:#999; border:1px solid #ddd;"

    def step_label(n):
        if n < step:
            return "✓"
        return str(n)

    st.markdown(f"""
    <div class="step-bar">
        <div class="step-dot" style="{step_color(1)}">{step_label(1)}</div>
        <div class="step-line"></div>
        <div class="step-dot" style="{step_color(2)}">{step_label(2)}</div>
        <div class="step-line"></div>
        <div class="step-dot" style="{step_color(3)}">{step_label(3)}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STEP 1: City + Country search ───────────────────────────────
    if step == 1:
        st.markdown('<p class="section-label">Step 1 — Location</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            city = st.text_input("City name", placeholder="e.g. Panaji, Mumbai, Delhi", label_visibility="collapsed")
        with col2:
            country_code = st.text_input("Country code", value="IN", label_visibility="collapsed")

        if st.button("🔍 Search"):
            if not city:
                st.warning("Please enter a city name.")
            else:
                import requests
                geo_url = (
                    f"https://geocoding-api.open-meteo.com/v1/search?"
                    f"name={city.strip()}&count=10&language=en&format=json"
                )
                try:
                    geo_resp = requests.get(geo_url, timeout=10).json()
                    matched = [
                        r for r in geo_resp.get("results", [])
                        if r.get("country_code", "").upper() == country_code.strip().upper()
                    ]
                except Exception:
                    matched = []

                if not matched:
                    st.error(f"No results found for '{city}' in '{country_code}'.")
                else:
                    unique_states = list(dict.fromkeys(r.get("admin1", "Unknown") for r in matched))
                    st.session_state["lw_matched_states"] = unique_states
                    st.session_state["lw_city"] = city.strip()
                    st.session_state["lw_country"] = country_code.strip().upper()
                    st.session_state["lw_step"] = 2
                    st.rerun()

    # ── STEP 2: State selector ──────────────────────────────────────
    elif step == 2:
        st.markdown('<p class="section-label">Step 2 — Select state</p>', unsafe_allow_html=True)

        unique_states = st.session_state["lw_matched_states"]
        city = st.session_state["lw_city"]

        if len(unique_states) > 1:
            selected_state = st.selectbox(
                f"Multiple matches for '{city}' — pick your state:",
                options=unique_states
            )
        else:
            selected_state = unique_states[0]
            st.info(f"Found: **{city}, {selected_state}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back"):
                st.session_state["lw_step"] = 1
                st.rerun()
        with col2:
            if st.button("☁️ Fetch Weather & Predict"):
                with st.spinner("Fetching live weather data..."):
                    weather = get_weather_data(
                        location=city,
                        country_code=st.session_state["lw_country"],
                        state=selected_state
                    )
                st.session_state["lw_weather"] = weather
                st.session_state["lw_selected_state"] = selected_state
                st.session_state["lw_step"] = 3
                st.rerun()

    # ── STEP 3: Weather metrics + prediction ────────────────────────
    elif step == 3:
        weather = st.session_state["lw_weather"]
        city = st.session_state["lw_city"]
        country = st.session_state["lw_country"]
        state = st.session_state.get("lw_selected_state", "")

        # Location badge + change button
        col_loc, col_btn = st.columns([3, 1])
        with col_loc:
            st.markdown(
                f'<div class="location-badge">📍 {city}, {state} · {country}</div>',
                unsafe_allow_html=True
            )
        with col_btn:
            if st.button("↩ Change city"):
                st.session_state["lw_step"] = 1
                st.session_state["lw_weather"] = None
                st.rerun()

        st.write("")

        # ── Temperature ─────────────────────────────────────────────
        st.markdown('<p class="section-label">🌡 Temperature</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Min Temp", f"{weather['MinTemp']} °C")
        with c2:
            st.metric("Max Temp", f"{weather['MaxTemp']} °C")
        with c3:
            st.metric("Rain Today", "Yes" if weather['RainToday'] else "No")

        # ── Humidity & Wind ─────────────────────────────────────────
        st.markdown('<p class="section-label">💧 Humidity & Wind</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Humidity 9am", f"{weather['Humidity9am']} %")
        with c2:
            st.metric("Humidity 3pm", f"{weather['Humidity3pm']} %")
        with c3:
            st.metric("Wind 9am", f"{weather['WindSpeed9am']} km/h")

        # ── Pressure ────────────────────────────────────────────────
        st.markdown('<p class="section-label">🔵 Pressure</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Pressure 9am", f"{weather['Pressure9am']} hPa")
        with c2:
            st.metric("Pressure 3pm", f"{weather['Pressure3pm']} hPa")
        with c3:
            st.metric("Wind 3pm", f"{weather['WindSpeed3pm']} km/h")

        st.divider()

        # ── Prediction ──────────────────────────────────────────────
        input_data = [
            weather["MinTemp"], weather["MaxTemp"],
            weather["Humidity9am"], weather["Humidity3pm"],
            weather["Pressure9am"], weather["Pressure3pm"],
            weather["Temp9am"], weather["Temp3pm"],
            weather["WindSpeed9am"], weather["WindSpeed3pm"],
            weather["RainToday"]
        ]

        result = predict_rain(input_data)

        st.subheader("Prediction Result")
        if result == 1:
            st.error("🌧️ It will RAIN tomorrow")
        else:
            st.success("☀️ No rain tomorrow")