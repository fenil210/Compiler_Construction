import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Grammar_FF import Grammar_FF
from Grammar_LR import Grammar_LR
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    st.set_page_config(page_title="Advanced Grammar Analysis Tool", page_icon="📚", layout="wide")

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", ["Home", "Find First Follow", "About"])

    if page == "Home":
        show_home()
    elif page == "Find First Follow":
        find_first_follow()
    else:
        show_about()

def show_home():
    st.title("Welcome to the First Follow Finding Tool")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        This tool helps you analyze context-free grammars, identify and eliminate left recursion,
        compute FIRST and FOLLOW sets, and remove LL(1) conflicts. Whether you're a student learning 
        about formal languages or a developer working on compiler design, this tool is here to assist you!
        """)
        
        st.info("Use the sidebar to navigate to different analysis tools.")
    
    with col2:
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=200)

def find_first_follow():
    st.title("Find First Follow")
    
    st.write("Enter the grammar rules. Use a new line for each rule.")
    st.write("Format: Non-terminal -> production1 | production2 | ...")
    
    rules = st.text_area("Grammar Rules", height=200)
    
    if st.button("Find First Follow"):
        if not rules:
            st.error("No grammar rules entered. Please input some rules.")
            return
        
        rules_list = [rule.strip() for rule in rules.split('\n') if rule.strip()]
        
        with st.spinner("Analyzing and removing LL(1) conflicts..."):
            grammar_lr = Grammar_LR(rules_list)
            
            if not grammar_lr.has_left_recursion():
                st.success("The given grammar does not have left recursion.")
            else:
                st.warning("The given grammar has left recursion. Eliminating...")
                grammar_lr.eliminate_left_recursion()
            
            st.subheader("Grammar after left recursion elimination:")
            st.code(str(grammar_lr))
            
            grammar_ff = Grammar_FF(grammar_lr)
            
            st.subheader("FIRST and FOLLOW sets:")
            st.code(str(grammar_ff))
            
            # Visualize symbol mapping
            st.subheader("Symbol Mapping:")
            df = pd.DataFrame(list(grammar_ff.symbol_mapping.items()), columns=['Symbol', 'Mapping'])
            st.dataframe(df)
            
            # Visualize FIRST and FOLLOW sets
            visualize_sets(grammar_ff)

    st.subheader("Example Grammar")
    st.code("""
    S -> ACB | CbB | Ba 
    A -> da | BC
    B -> g | ε
    C -> h | ε 
    """)
    st.code("""
            E -> E+T | T
            T -> T*F | F
            F -> (E) | i """)

def visualize_sets(grammar_ff):
    # Create a Sankey diagram for FIRST and FOLLOW sets
    source = []
    target = []
    value = []
    label = []

    for symbol, first_set in grammar_ff.FIRST.items():
        for item in first_set:
            source.append(symbol)
            target.append(f"FIRST: {item}")
            value.append(1)
        
    for symbol, follow_set in grammar_ff.FOLLOW.items():
        for item in follow_set:
            source.append(symbol)
            target.append(f"FOLLOW: {item}")
            value.append(1)

    label = list(set(source + target))

    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = label,
          color = "blue"
        ),
        link = dict(
          source = [label.index(src) for src in source],
          target = [label.index(tgt) for tgt in target],
          value = value
    ))])

    fig.update_layout(title_text="FIRST and FOLLOW Sets Visualization", font_size=10)
    st.plotly_chart(fig, use_container_width=True)

def show_about():
    st.title("About the Grammar Analysis Tool")
    st.write("""
    This tool was developed to assist in the analysis of context-free grammars.
    It provides functionality for:
    
    - Identifying and eliminating left recursion
    - Removing LL(1) conflicts
    - Computing FIRST and FOLLOW sets
    - Visualizing the relationships between symbols and their sets
    
    Whether you're a student studying compiler design or a developer working
    on language processing, we hope this tool proves useful in your endeavors.
    """)
    
    st.subheader("How to Use")
    st.write("""
    1. Use the sidebar to navigate between different analysis tools
    2. Enter your grammar rules in the provided text area
    3. Click the respective button to perform the analysis
    4. Explore the results and visualizations provided
    """)
    
    st.subheader("Feedback")
    st.write("""
    We're always looking to improve! If you have any suggestions or encounter any issues,
    please don't hesitate to reach out.
    """)
    
    if st.button("Provide Feedback"):
        st.text_area("Your Feedback", placeholder="Enter your feedback here...")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()