import streamlit as st
import itertools
import pandas as pd
from io import StringIO

# Triangular numbers under 39
TRIANGULAR_NUMBERS = {1, 3, 6, 10, 15, 21, 28, 36}

st.title("5-Number Generator with Custom Constraints")
st.write("Enter a pool of numbers separated by commas (5-8 numbers). Example: 1,2,3,4,5,6,7,8")

# Sidebar for custom constraints
st.sidebar.header("Custom Constraints")
odd_even_ratio = st.sidebar.selectbox(
    "Odd/Even Ratio",
    ["5/0", "4/1", "3/2", "2/3", "1/4", "0/5"]
)

sum_min = st.sidebar.number_input("Minimum Sum", min_value=5, max_value=195, value=50)
sum_max = st.sidebar.number_input("Maximum Sum", min_value=5, max_value=195, value=150)

triangular_allowed = st.sidebar.radio(
    "Max Triangular Numbers per Row",
    [0, 1, 2]
)

dataset_count = st.sidebar.number_input(
    "Number of datasets to generate",
    min_value=1, max_value=500, value=10
)

# User input
user_input = st.text_input("Enter your numbers separated by commas:")

if st.button("Generate Combinations"):
    try:
        numbers = sorted(set(int(num.strip()) for num in user_input.split(",")))
        if len(numbers) < 5:
            st.warning("⚠️ Please enter at least 5 numbers.")
        elif len(numbers) > 8:
            st.warning("⚠️ You can enter at most 8 numbers.")
        else:
            # Count odd and even numbers in the pool
            total_odd = sum(1 for n in numbers if n % 2 != 0)
            total_even = len(numbers) - total_odd

            o, e = map(int, odd_even_ratio.split("/"))

            # Check if pool can satisfy the selected ratio
            if total_odd < o or total_even < e:
                st.warning(
                    f"⚠️ Your pool cannot satisfy the {o}/{e} odd/even ratio. "
                    f"Odd numbers in pool: {total_odd}, Even numbers in pool: {total_even}"
                )
            else:
                # Generate all 5-number combinations
                all_combos = list(itertools.combinations(numbers, 5))
                filtered_combos = []
                
                for combo in all_combos:
                    odd_count = sum(1 for n in combo if n % 2 != 0)
                    even_count = 5 - odd_count
                    if odd_count == o and even_count == e:
                        tri_count = sum(1 for n in combo if n in TRIANGULAR_NUMBERS)
                        if tri_count <= triangular_allowed:
                            combo_sum = sum(combo)
                            if sum_min <= combo_sum <= sum_max:
                                filtered_combos.append(combo)
                
                # Limit to dataset_count
                filtered_combos = filtered_combos[:dataset_count]
                
                if filtered_combos:
                    df = pd.DataFrame(filtered_combos, columns=["Num1","Num2","Num3","Num4","Num5"])
                    df["Sum"] = df.sum(axis=1)
                    st.success(f"Generated {len(filtered_combos)} dataset(s)")
                    st.dataframe(df)

                    # Download CSV
                    csv_buffer = StringIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_bytes = csv_buffer.getvalue().encode()
                    st.download_button(
                        label="Download CSV",
                        data=csv_bytes,
                        file_name="generated_5_number_datasets.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No combinations matched the selected constraints.")
                
    except ValueError:
        st.error("⚠️ Please enter only numbers separated by commas.")
