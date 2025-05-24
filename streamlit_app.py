import streamlit as st
import pandas as pd

st.set_page_config(page_title="Situation test rappels de paiements mensuel", layout="wide")

st.title("📊 Situation des rappels de paiements mensuel")
st.markdown("Upload your Excel file to calculate totals")

def main():
    uploaded_file = st.file_uploader("Choose XLSX file", type=["xlsx"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            # Clean data
            df_clean = df.dropna(subset=['Nom']).copy()  # Remove empty rows
            
            # Convert to numeric
            df_clean['Montant dû'] = pd.to_numeric(df_clean['Montant dû'], errors='coerce')
            df_clean['Dettes en recouvrement'] = pd.to_numeric(df_clean['Dettes en recouvrement'], errors='coerce')
            
            # Calculate totals
            total_d = df_clean['Montant dû'].sum()
            total_e = df_clean['Dettes en recouvrement'].sum()
            row_count = len(df_clean)
            
            # Display results
            st.success("✅ File processed successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Amount Due", f"€ {total_d:,.2f}", help="Sum of Column D")
            with col2:
                st.metric("Total Collection Debt", f"€ {total_e:,.2f}", help="Sum of Column E")
            with col3:
                st.metric("Valid Records", row_count, help="Rows with client names")
            
            # Show data preview
            st.subheader("Data Preview")
            st.dataframe(df_clean.style.format({
                'Montant dû': '€ {:.2f}',
                'Dettes en recouvrement': '€ {:.2f}'
            }), height=400)

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
