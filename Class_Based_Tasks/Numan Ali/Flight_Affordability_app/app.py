import os
import requests
import pandas as pd
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="Smart Flight Finder",
    page_icon="✈️",
    layout="wide"
)


# Demo data 

DEMO_FLIGHTS = [
    {
        "airline": "Airblue",
        "flight": "PA-401",
        "departure": "09:00",
        "arrival": "10:55",
        "duration": "1h 55m",
        "stops": 0,
        "price": 18250,
        "currency": "PKR"
    },
    {
        "airline": "AirSial",
        "flight": "PF-142",
        "departure": "11:30",
        "arrival": "13:25",
        "duration": "1h 55m",
        "stops": 0,
        "price": 18465,
        "currency": "PKR"
    },
    {
        "airline": "PIA",
        "flight": "PK-303",
        "departure": "14:00",
        "arrival": "15:55",
        "duration": "1h 55m",
        "stops": 0,
        "price": 18711,
        "currency": "PKR"
    },
    {
        "airline": "Fly Jinnah",
        "flight": "9P-849",
        "departure": "17:10",
        "arrival": "19:05",
        "duration": "1h 55m",
        "stops": 0,
        "price": 19064,
        "currency": "PKR"
    },
]

AIRPORTS = {
    "Lahore (LHE)": "LHE",
    "Karachi (KHI)": "KHI",
    "Islamabad (ISB)": "ISB",
    "Dubai (DXB)": "DXB",
    "Abu Dhabi (AUH)": "AUH",
    "Doha (DOH)": "DOH",
    "Riyadh (RUH)": "RUH",
    "Jeddah (JED)": "JED",
    "London (LHR)": "LHR",
}

def get_live_flights(origin, destination, travel_date, currency="PKR"):
    # Fetch Google Flights-style results through SerpApi.
    api_key = st.secrets.get("SERPAPI_KEY", os.getenv("SERPAPI_KEY"))

    if not api_key:
        return None, "No SERPAPI_KEY found."

    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": str(travel_date),
        "type": "2",          # one-way
        "currency": currency,
        "hl": "en",
        "api_key": api_key,
    }

    try:
        response = requests.get(
            "use your API",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        flights = []

        for group_name in ["best_flights", "other_flights"]:
            for item in data.get(group_name, []):
                segments = item.get("flights", [])
                if not segments:
                    continue

                first = segments[0]
                last = segments[-1]

                price = item.get("price")
                if price is None:
                    continue

                flights.append({
                    "airline": first.get("airline", "Unknown"),
                    "flight": first.get("flight_number", "N/A"),
                    "departure": first.get("departure_airport", {}).get("time", "")[-5:],
                    "arrival": last.get("arrival_airport", {}).get("time", "")[-5:],
                    "duration": f"{item.get('total_duration', 0)//60}h {item.get('total_duration', 0)%60}m",
                    "stops": max(len(segments) - 1, 0),
                    "price": int(price),
                    "currency": currency,
                })

        if not flights:
            return [], "No flights returned for this route/date."

        return flights, None

    except Exception as e:
        return None, str(e)



# UI

st.title("✈️ Smart Flight Finder")
st.caption("Find flights according to your route, date and personal budget.")

with st.sidebar:
    st.header("Search")

    origin_name = st.selectbox(
        "From Airport",
        list(AIRPORTS.keys()),
        index=0
    )

    destination_options = [
        name for name in AIRPORTS.keys() if name != origin_name
    ]

    destination_name = st.selectbox(
        "To Airport",
        destination_options,
        index=1 if len(destination_options) > 1 else 0
    )

    travel_date = st.date_input(
        "Travel Date",
        value=date.today() + timedelta(days=1),
        min_value=date.today()
    )

    budget = st.number_input(
        "Your Maximum Budget (PKR)",
        min_value=10000,
        max_value=5000000,
        value=20000,
        step=1000
    )

    passengers = st.number_input(
        "Passengers",
        min_value=1,
        max_value=9,
        value=1,
        step=1
    )

    live_mode = st.toggle(
        "Use Live Flight Data",
        value=True
    )

    search = st.button(
        "🔎 Find Affordable Flights",
        use_container_width=True,
        type="primary"
    )

if search:
    origin = AIRPORTS[origin_name]
    destination = AIRPORTS[destination_name]

    st.subheader(
        f"{origin_name} → {destination_name}"
    )

    with st.spinner("Searching current flight offers..."):
        if live_mode:
            flights, error = get_live_flights(
                origin,
                destination,
                travel_date
            )

            if flights is None:
                st.warning(
                    "Live API unavailable. Presentation demo data is being used."
                )
                flights = DEMO_FLIGHTS
                error_message = error
            else:
                error_message = None
        else:
            flights = DEMO_FLIGHTS
            error_message = None

    df = pd.DataFrame(flights)

    # Total cost for all passengers
    df["total_price"] = df["price"] * passengers
    df["budget_status"] = df["total_price"].apply(
        lambda x: "✅ Affordable" if x <= budget else "❌ Over Budget"
    )

    # Affordable flights first, then cheapest
    df["affordable"] = df["total_price"] <= budget
    df = df.sort_values(
        by=["affordable", "total_price"],
        ascending=[False, True]
    ).reset_index(drop=True)

    affordable = df[df["affordable"]]


    # Recommendation

    if not affordable.empty:
        best = affordable.iloc[0]

        st.success(
            f"🎯 Best affordable option: {best['airline']} {best['flight']} "
            f"for PKR {best['total_price']:,}"
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Best Price", f"PKR {best['total_price']:,}")
        c2.metric(
            "Budget Remaining",
            f"PKR {budget - best['total_price']:,}"
        )
        c3.metric("Stops", int(best["stops"]))
    else:
        cheapest = df.iloc[0]
        shortage = int(cheapest["total_price"] - budget)

        st.error(
            f"❌ No flight fits your budget. Cheapest option is "
            f"PKR {cheapest['total_price']:,}; you need PKR {shortage:,} more."
        )

    st.divider()
    st.subheader("Available Flights")

    display_df = df[
        [
            "airline",
            "flight",
            "departure",
            "arrival",
            "duration",
            "stops",
            "price",
            "total_price",
            "budget_status",
        ]
    ].copy()

    display_df.columns = [
        "Airline",
        "Flight",
        "Departure",
        "Arrival",
        "Duration",
        "Stops",
        "Price / Person",
        "Total Price",
        "Budget"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "⚠️ Flight prices are dynamic. Always verify the final fare on the booking provider before payment."
    )

else:
    st.info(
        "👈 Enter your route, travel date and budget, then click "
        "'Find Affordable Flights'."
    )