import streamlit as st
import pickle
import numpy as np
import requests

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def get_exchange_rate(from_currency, to_currency="USD"):
    url = "https://currency-converter18.p.rapidapi.com/api/v1/convert"
    querystring = {"from": from_currency, "to": to_currency, "amount": "1"}
    headers = {
        "X-RapidAPI-Key": "e021a002e9msh6218c60a48e1248p1628b9jsn5c170bb85457",
        "X-RapidAPI-Host": "currency-converter18.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        return data['result']['convertedAmount']
    else:
        st.error("Error fetching exchange rate")
        return 1.0

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("### We need some information to predict the salary")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        if experience == 0:
            st.subheader("Can't predict, developer just graduated.")
        else:
            X = np.array([[country, education, experience]])
            X[:, 0] = le_country.transform(X[:, 0])
            X[:, 1] = le_education.transform(X[:, 1])
            X = X.astype(float)

            salary_usd = regressor.predict(X)[0]

            currency_code = {
                "United States": "USD",
                "India": "INR",
                "United Kingdom": "GBP",
                "Germany": "EUR",
                "Canada": "CAD",
                "Brazil": "BRL",
                "France": "EUR",
                "Spain": "EUR",
                "Australia": "AUD",
                "Netherlands": "EUR",
                "Poland": "PLN",
                "Italy": "EUR",
                "Russian Federation": "RUB",
                "Sweden": "SEK"
            }

            local_currency = currency_code[country]
            exchange_rate = get_exchange_rate("USD", local_currency)
            
            salary_local = salary_usd * exchange_rate

            st.subheader(f"The estimated salary is {salary_local:.2f} {local_currency}")
