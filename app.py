import streamlit as st
import itertools
import pandas as pd

st.title("5-Number Generator")
st.write("Enter a pool of numbers separated by commas. You must enter **at least 5 numbers and at most 8 numbers**. Example: 1,2,3,4,5,6,7,8")

# User input: numbers separated by commas
user_input = st.text_input("Enter your numbers separated by commas:")

# Button to generate combinations
if st.button("Generate Combinations"):
    try:
        # Convert input string to a sorted list of unique integers
        numbers = sorted(set(int(num.strip()) for num in user_input.split(",")))
        
        # Validate input
        if len(numbers) < 5:
            st.warning("⚠️ Please enter at least 5 numbers.")
        elif len(numbers) > 8:
            st.warning("⚠️ You can enter at most 8 numbers.")
        else:
            # Generate all 5-number combinations
            combos = list(itertools.combinations(numbers, 5))
            
            st.success(f"Total combinations generated: {len(combos)}")
            
            # Convert to DataFrame for better display
            df_combos = pd.DataFrame(combos, columns=["Num1", "Num2", "Num3", "Num4", "Num5"])
            
            # Display the table
            st.dataframe(df_combos)
                
    except ValueError:
        st.error("⚠️ Please make sure you enter only numbers separated by commas.")
