import streamlit as st
import pandas as pd

st.set_page_config(page_title="Situation des rappel", layout="wide")

st.title("📊 Situation des rappels de paiements")
st.markdown("Upload your Excel file to calculate totals")

def main():
    uploaded_file = st.file_uploader("Choose XLSX file", type=["xlsx"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            # Clean data
            df_clean = df.dropna(subset=['Nom']).copy()  # Remove empty rows
            
            # Initialize metrics list
            metrics = []
            
            # Process columns if they exist
            if 'Montant dû' in df_clean.columns:
                df_clean['Montant dû'] = pd.to_numeric(df_clean['Montant dû'], errors='coerce')
                total_d = df_clean['Montant dû'].sum()
                metrics.append(('Montant dû', f"€ {total_d:,.2f}", "Sum of Column D"))
            
            if 'Dettes en recouvrement' in df_clean.columns:
                df_clean['Dettes en recouvrement'] = pd.to_numeric(df_clean['Dettes en recouvrement'], errors='coerce')
                total_e = df_clean['Dettes en recouvrement'].sum()
                metrics.append(('Plan de paiement en cours', f"€ {total_e:,.2f}", "Sum of Column E"))
            
            # Always show row count
            metrics.append(('Nombre de personnes', len(df_clean), "Rows with client names"))
            
            # Display results
            st.success("✅ File processed successfully!")
            
            # Create dynamic columns
            num_cols = len(metrics)
            cols = st.columns(num_cols)
            for i, (label, value, help_text) in enumerate(metrics):
                with cols[i]:
                    st.metric(label, value, help=help_text)
            
            # Show data preview with conditional formatting
            st.subheader("Data Preview")
            format_dict = {}
            if 'Montant dû' in df_clean.columns:
                format_dict['Montant dû'] = '€ {:.2f}'
            if 'Dettes en recouvrement' in df_clean.columns:
                format_dict['Dettes en recouvrement'] = '€ {:.2f}'
            
            if format_dict:
                st.dataframe(df_clean.style.format(format_dict), height=400)
            else:
                st.dataframe(df_clean, height=400)

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
