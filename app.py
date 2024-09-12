import streamlit as st
from Grammar_FF import Grammar_FF
from Grammar_LR import Grammar_LR

def main():
    st.title("Grammar Analysis Tool")
    st.write("Enter the grammar rules. Use a new line for each rule.")
    st.write("Format: Non-terminal -> production1 | production2 | ...")
    
    rules = st.text_area("Grammar Rules", height=200)
    
    if st.button("Analyze Grammar"):
        if not rules:
            st.error("No grammar rules entered. Please input some rules.")
            return
        
        rules_list = [rule.strip() for rule in rules.split('\n') if rule.strip()]
        
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
        
        st.subheader("Symbol Mapping:")
        st.json(grammar_ff.symbol_mapping)

if __name__ == "__main__":
    main()