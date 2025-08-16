import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="📍 Location-Based Restaurant Analysis", layout="wide")
st.title("📍 Location-Based Restaurant Analysis")

# 1️⃣ Load dataset function (defined before calling)
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset .csv")
 # Ensure file name matches exactly
    return df

# 2️⃣ Call the function to load data
df = load_data()

# 3️⃣ Preview dataset
st.subheader("Preview of Dataset")
st.dataframe(df.head())

# 4️⃣ Identify city/locality column
city_col = None
for col in df.columns:
    if "city" in col.lower() or "locality" in col.lower():
        city_col = col
        break

if city_col is None:
    st.error("No column found for City/Locality. Please check your dataset.")
else:
    # Dropdown for city/locality selection
    cities = df[city_col].dropna().unique()
    selected_city = st.selectbox("Select a city/locality to analyze:", sorted(cities))

    filtered_df = df[df[city_col].str.contains(selected_city, case=False, na=False)]

    if filtered_df.empty:
        st.warning(f"No restaurants found for '{selected_city}'")
    else:
        st.success(f"Found {len(filtered_df)} restaurants in {selected_city}")

        # 5️⃣ Display statistics
        st.subheader(f"Statistics for {selected_city}")
        if "Rating" in df.columns:
            avg_rating = filtered_df["Rating"].mean()
            st.write(f"⭐ Average Rating: {avg_rating:.2f}")

        if "Price range" in df.columns:
            avg_price = filtered_df["Price range"].mean()
            st.write(f"💰 Average Price Range: {avg_price:.2f}")

        if "Cuisines" in df.columns:
            st.write("🍽️ Top 10 Popular Cuisines:")
            st.write(filtered_df["Cuisines"].value_counts().head(10))

        # 6️⃣ Restaurant count chart
        st.subheader("Restaurant Count by Cuisines")
        cuisine_counts = filtered_df["Cuisines"].value_counts().head(10)
        fig, ax = plt.subplots()
        cuisine_counts.plot(kind='barh', ax=ax, color='skyblue')
        ax.set_xlabel("Number of Restaurants")
        ax.set_ylabel("Cuisine")
        st.pyplot(fig)

        # 7️⃣ Rating distribution histogram
        if "Rating" in df.columns:
            st.subheader("Rating Distribution")
            fig2, ax2 = plt.subplots()
            filtered_df["Rating"].hist(bins=10, ax=ax2, color='lightgreen')
            ax2.set_xlabel("Rating")
            ax2.set_ylabel("Number of Restaurants")
            st.pyplot(fig2)

        # 8️⃣ Interactive map using Folium
        if "Latitude" in df.columns and "Longitude" in df.columns:
            st.subheader("🗺️ Restaurant Map")
            m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=12)

            for _, row in filtered_df.iterrows():
                popup_text = f"Name: {row.get('Name', 'N/A')}<br>"
                if "Cuisines" in row: popup_text += f"Cuisines: {row['Cuisines']}<br>"
                if "Rating" in row: popup_text += f"Rating: {row['Rating']}"
                folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=popup_text).add_to(m)

            st_data = st_folium(m, width=700, height=500)
