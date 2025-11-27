"""
MEL Compiler - Streamlit Web Application
Run with: streamlit run app.py
"""

import streamlit as st
import json
from compiler import (
    MELCompiler, 
    TokenType, 
    Token,
    Lexer,
    Parser,
    SemanticAnalyzer,
    IntermediateCodeGenerator,
    Optimizer,
    Interpreter
)

# Page configuration
st.set_page_config(
    page_title="MEL Compiler",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 8px;
        color: white;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #7c3aed;
    }
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .phase-card {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #7c3aed;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ef4444;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⚙️ MEL Compiler</h1>
    <p style="font-size: 1.2rem; margin: 0;">Mathematical Expression Language - Complete 6-Phase Compiler</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with examples
st.sidebar.title("📚 Example Programs")
st.sidebar.markdown("---")

examples = {
    "Fibonacci Sequence": """# Fibonacci sequence generator
var n = 10;
var a = 0;
var b = 1;
var i = 0;

while (i < n) {
    print(a);
    var temp = a + b;
    a = b;
    b = temp;
    i = i + 1;
}

print("Done!");""",
    
    "Factorial Calculator": """# Factorial calculator
var n = 5;
var result = 1;
var i = 1;

while (i <= n) {
    result = result * i;
    i = i + 1;
}

print("Factorial of");
print(n);
print("is");
print(result);""",
    
    "Sum of Numbers": """# Sum of first N numbers
var n = 100;
var sum = 0;
var i = 1;

while (i <= n) {
    sum = sum + i;
    i = i + 1;
}

print("Sum of first");
print(n);
print("numbers is");
print(sum);""",
    
    "Even/Odd Counter": """# Count even and odd numbers
var n = 20;
var i = 1;
var even = 0;
var odd = 0;

while (i <= n) {
    var remainder = i - ((i / 2) * 2);
    if (remainder == 0) {
        even = even + 1;
    } else {
        odd = odd + 1;
    }
    i = i + 1;
}

print("Even:");
print(even);
print("Odd:");
print(odd);""",
    
    "Power Calculator": """# Calculate power (x^y)
var base = 2;
var exponent = 10;
var result = 1;
var i = 0;

while (i < exponent) {
    result = result * base;
    i = i + 1;
}

print("Result:");
print(result);"""
}

# Example selection
selected_example = st.sidebar.selectbox(
    "Choose an example:",
    ["Custom Code"] + list(examples.keys())
)

# Language specification in sidebar
st.sidebar.markdown("---")
st.sidebar.title("📖 Language Specification")
with st.sidebar.expander("Keywords"):
    st.code("var, if, else, while, for, print, function, return")

with st.sidebar.expander("Operators"):
    st.code("+, -, *, /, =, ==, !=, <, >, <=, >=, &&, ||")

with st.sidebar.expander("Data Types"):
    st.markdown("- **Numbers**: Integers and floats\n- **Strings**: Text in quotes\n- **Booleans**: 0 (false), 1 (true)")

# Initialize session state
if 'compiled' not in st.session_state:
    st.session_state.compiled = False
if 'result' not in st.session_state:
    st.session_state.result = None

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Source Code Editor")
    
    # Get initial code
    if selected_example == "Custom Code":
        default_code = examples["Fibonacci Sequence"]
    else:
        default_code = examples[selected_example]
    
    # Code editor
    source_code = st.text_area(
        "Write your MEL code here:",
        value=default_code,
        height=400,
        key="code_editor"
    )
    
    # Compile button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        compile_button = st.button("🚀 Compile & Run", type="primary", use_container_width=True)
    with col_btn2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.compiled = False
        st.session_state.result = None
        st.rerun()
    
    if compile_button:
        with st.spinner("Compiling..."):
            compiler = MELCompiler(source_code)
            st.session_state.result = compiler.compile_and_run()
            st.session_state.compiled = True

with col2:
    st.subheader("📊 Compilation Results")
    
    if st.session_state.compiled and st.session_state.result:
        result = st.session_state.result
        
        if result['success']:
            st.markdown('<div class="success-box">✅ Compilation Successful!</div>', unsafe_allow_html=True)
            
            # Tabs for different phases
            tabs = st.tabs([
                "🖥️ Output", 
                "🔤 Tokens", 
                "🌳 AST", 
                "📊 Symbols", 
                "⚙️ TAC", 
                "⚡ Optimized"
            ])
            
            # Tab 1: Output
            with tabs[0]:
                st.markdown("### Program Output")
                if result['output']:
                    output_lines = result['output'].split('\n')
                    st.code('\n'.join(output_lines), language='text')
                else:
                    st.info("No output generated")
            
            # Tab 2: Tokens
            with tabs[1]:
                st.markdown("### Lexical Analysis - Tokens")
                st.caption(f"Total tokens: {len(result['tokens'])}")
                
                # Display tokens in a nice format
                token_data = []
                for i, token in enumerate(result['tokens'][:50]):  # Limit to first 50
                    if token.type != TokenType.EOF and token.type != TokenType.COMMENT:
                        token_data.append({
                            "#": i+1,
                            "Type": token.type.value,
                            "Value": token.value,
                            "Line": token.line,
                            "Column": token.column
                        })
                
                if token_data:
                    st.dataframe(token_data, use_container_width=True, hide_index=True)
                
                if len(result['tokens']) > 50:
                    st.info(f"Showing first 50 of {len(result['tokens'])} tokens")
            
            # Tab 3: AST
            with tabs[2]:
                st.markdown("### Syntax Analysis - Abstract Syntax Tree")
                st.caption(f"Total AST nodes: {len(result['ast'])}")
                
                def format_ast_node(node, indent=0):
                    """Format AST node for display"""
                    lines = []
                    prefix = "  " * indent
                    
                    if hasattr(node, 'type'):
                        lines.append(f"{prefix}• {node.type}")
                        
                        if hasattr(node, '__dict__'):
                            for key, value in node.__dict__.items():
                                if key != 'type' and value is not None:
                                    if isinstance(value, list):
                                        lines.append(f"{prefix}  {key}:")
                                        for item in value:
                                            lines.extend(format_ast_node(item, indent + 2))
                                    elif hasattr(value, 'type'):
                                        lines.append(f"{prefix}  {key}:")
                                        lines.extend(format_ast_node(value, indent + 2))
                                    else:
                                        lines.append(f"{prefix}  {key}: {value}")
                    
                    return lines
                
                ast_text = []
                for node in result['ast'][:10]:  # Show first 10 nodes
                    ast_text.extend(format_ast_node(node))
                    ast_text.append("")  # Blank line between nodes
                
                st.code('\n'.join(ast_text), language='text')
                
                if len(result['ast']) > 10:
                    st.info(f"Showing first 10 of {len(result['ast'])} AST nodes")
            
            # Tab 4: Symbol Table
            with tabs[3]:
                st.markdown("### Semantic Analysis - Symbol Table")
                st.caption(f"Total symbols: {len(result['symbols'])}")
                
                symbol_data = []
                for symbol in result['symbols']:
                    symbol_data.append({
                        "Name": symbol.name,
                        "Type": symbol.type,
                        "Scope": symbol.scope,
                        "Declared": "✓" if symbol.declared else "✗",
                        "Status": symbol.error if symbol.error else "OK"
                    })
                
                if symbol_data:
                    st.dataframe(symbol_data, use_container_width=True, hide_index=True)
                else:
                    st.info("No symbols in table")
                
                if result['errors']:
                    st.error("**Semantic Errors:**")
                    for error in result['errors']:
                        st.write(f"- {error}")
            
            # Tab 5: Three-Address Code
            with tabs[4]:
                st.markdown("### Intermediate Code Generation")
                st.caption(f"Total instructions: {len(result['intermediate_code'])}")
                
                if result['intermediate_code']:
                    tac_text = '\n'.join(
                        f"{i+1:3d}: {line}" 
                        for i, line in enumerate(result['intermediate_code'])
                    )
                    st.code(tac_text, language='text')
                else:
                    st.info("No intermediate code generated")
            
            # Tab 6: Optimized Code
            with tabs[5]:
                st.markdown("### Code Optimization")
                st.caption(f"Total instructions: {len(result['optimized_code'])}")
                
                if result['optimized_code']:
                    opt_text = '\n'.join(
                        f"{i+1:3d}: {line}" 
                        for i, line in enumerate(result['optimized_code'])
                    )
                    st.code(opt_text, language='text')
                    
                    # Show optimization statistics
                    original_count = len(result['intermediate_code'])
                    optimized_count = len(result['optimized_code'])
                    
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    with col_stat1:
                        st.metric("Original Instructions", original_count)
                    with col_stat2:
                        st.metric("Optimized Instructions", optimized_count)
                    with col_stat3:
                        reduction = original_count - optimized_count
                        st.metric("Instructions Saved", reduction)
                else:
                    st.info("No optimized code generated")
        
        else:
            st.markdown(f'<div class="error-box">❌ Compilation Failed<br>{result["error"]}</div>', 
                       unsafe_allow_html=True)
            st.code(result['output'], language='text')
    
    else:
        st.info("👈 Click 'Compile & Run' to see results")
        
        # Show compiler phases overview
        st.markdown("### Compiler Phases")
        
        phases = [
            ("1️⃣ Lexical Analysis", "Tokenizes source code into meaningful symbols"),
            ("2️⃣ Syntax Analysis", "Builds Abstract Syntax Tree (AST)"),
            ("3️⃣ Semantic Analysis", "Checks variable declarations and types"),
            ("4️⃣ Intermediate Code", "Generates three-address code"),
            ("5️⃣ Optimization", "Performs constant folding and propagation"),
            ("6️⃣ Code Generation", "Executes the optimized program")
        ]
        
        for phase, description in phases:
            with st.container():
                st.markdown(f"""
                <div class="phase-card">
                    <strong>{phase}</strong><br>
                    <small style="color: #94a3b8;">{description}</small>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; padding: 1rem;">
    <strong>MEL Compiler</strong> - A complete 6-phase compiler implementation<br>
    Developed for Compiler Construction Course
</div>
""", unsafe_allow_html=True)