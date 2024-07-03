import os
import streamlit as st
import pandas as pd
from google.cloud import firestore

# Set up the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Insert Google json file"

# Initialize Firestore client
db = firestore.Client()

def fetch_data_from_firestore(collection_name):
    """Fetches data from the specified Firestore collection."""
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    
    return data

def main():
    st.title("Expogenix Attendance List")

    collection_name = "attendance"  # Replace with your collection name

    # Fetch data from Firestore
    data = fetch_data_from_firestore(collection_name)
    
    if data:
        # Convert data to DataFrame and ensure the columns are in the correct order
        df = pd.DataFrame(data)
        columns_order = ["roll_no", "name","branch", "result"]
        
        # Check if all expected columns are present
        if all(column in df.columns for column in columns_order):
            df = df[columns_order]
        else:
            st.error("Missing expected columns in the data.")
            return
        df.insert(0, 'Presentee No.', range(1, len(df) + 1))
        # Display data in Streamlit
        # st.write("### Attendance Data")
        st.dataframe(df,use_container_width=True,hide_index=True)
    else:
        st.write("No data found in the Firestore collection.")

if __name__ == "__main__":
    main()
