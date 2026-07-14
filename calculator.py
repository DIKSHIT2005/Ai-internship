import streamlit as st

st.title("Simple Calculator")

a = st.number_input("First Number")
b = st.number_input("Second Number")

op = st.selectbox("Operation", ["+", "-", "*", "/"])

if st.button("Calculate"):
    if op == "+":
        st.write("Result:", a + b)
    elif op == "-":
        st.write("Result:", a - b)
    elif op == "*":
        st.write("Result:", a * b)
    elif op == "/":
        if b != 0:
            st.write("Result:", a / b)
        else:
            st.write("Cannot divide by zero")