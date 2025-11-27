# MEL Compiler - Mathematical Expression Language

## Project Overview

A complete **6-phase compiler** implementation for MEL (Mathematical Expression Language), a domain-specific language designed for mathematical computations with variables, control flow, and I/O operations.

### Team Members
- Waniya Syed (22k-4516)
- Haneesh Ali Rizvi (22k-4240)
- Valihasan Jalees (22k-4426)

### Course Information
- **Course**: Compiler Construction
- **Date**: November 26, 2025
- **Instructor**: [Zulfiquar Ali]

---

## Table of Contents

1. [Language Specification](#language-specification)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Compiler Phases](#compiler-phases)
5. [Project Structure](#project-structure)
6. [Test Cases](#test-cases)
7. [Deliverables](#deliverables)

---

## Language Specification

### Purpose
MEL is designed for mathematical expression evaluation and numerical computations. It supports:
- Variable declarations and assignments
- Arithmetic operations (+, -, *, /)
- Comparison operators (<, >, <=, >=, ==, !=)
- Logical operators (&&, ||)
- Control flow (if/else, while loops)
- Print statements for output

### Keywords
```
var, if, else, while, for, print, function, return
```

### Data Types
- **Numbers**: Integers and floating-point numbers (e.g., 42, 3.14)
- **Strings**: Text enclosed in double quotes (e.g., "Hello")
- **Booleans**: Represented as 0 (false) or 1 (true)

### Operators

**Arithmetic:**
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division

**Comparison:**
- `<` Less than
- `>` Greater than
- `<=` Less than or equal
- `>=` Greater than or equal
- `==` Equal to
- `!=` Not equal to

**Logical:**
- `&&` Logical AND
- `||` Logical OR

**Assignment:**
- `=` Assignment operator

### Syntax Examples

#### Variable Declaration
```mel
var x = 10;
var name = "Alice";
var result = 5 + 3;
```

#### Assignment
```mel
x = x + 1;
counter = counter * 2;
```

#### While Loop
```mel
while (i < 10) {
    print(i);
    i = i + 1;
}
```

#### If-Else Statement
```mel
if (x > y) {
    max = x;
} else {
    max = y;
}
```

#### Print Statement
```mel
print(result);
print("Hello World");
```

### Grammar (BNF)

```bnf
<program>        ::= <statement>*

<statement>      ::= <var_decl> | <assignment> | <while_loop> 
                   | <if_statement> | <print_statement>

<var_decl>       ::= "var" <identifier> "=" <expression> ";"

<assignment>     ::= <identifier> "=" <expression> ";"

<while_loop>     ::= "while" "(" <expression> ")" "{" <statement>* "}"

<if_statement>   ::= "if" "(" <expression> ")" "{" <statement>* "}"
                     ["else" "{" <statement>* "}"]

<print_statement>::= "print" "(" <expression> ")" ";"

<expression>     ::= <logical_or>

<logical_or>     ::= <logical_and> ("||" <logical_and>)*

<logical_and>    ::= <equality> ("&&" <equality>)*

<equality>       ::= <comparison> (("==" | "!=") <comparison>)*

<comparison>     ::= <additive> (("<" | ">" | "<=" | ">=") <additive>)*

<additive>       ::= <multiplicative> (("+" | "-") <multiplicative>)*

<multiplicative> ::= <primary> (("*" | "/") <primary>)*

<primary>        ::= <number> | <string> | <identifier> 
                   | "(" <expression> ")"
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (or extract the zip file):
```bash
cd mel-compiler
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify installation**:
```bash
python compiler.py
```

---

## Usage

### Running the Streamlit Web Application

The easiest way to use the compiler is through the web interface:

```bash
streamlit run app.py
```

This will open a browser window with the MEL Compiler interface where you can:
- Write or select example programs
- Compile and run code
- View all compilation phases
- See detailed results for each phase

### Using the Compiler Programmatically

```python
from compiler import MELCompiler

# Create source code
source_code = """
var n = 10;
var sum = 0;
var i = 1;

while (i <= n) {
    sum = sum + i;
    i = i + 1;
}

print(sum);
"""

# Compile and run
compiler = MELCompiler(source_code)
result = compiler.compile_and_run()

if result['success']:
    print("Output:", result['output'])
    print("Tokens:", len(result['tokens']))
    print("AST Nodes:", len(result['ast']))
else:
    print("Error:", result['error'])
```

### Command Line Testing

```bash
# Run the example in compiler.py
python compiler.py

# This will execute the Fibonacci example and show all phases
```

---

## Compiler Phases

### Phase 1: Lexical Analysis
**Purpose**: Convert source code into tokens

**Input**: Source code string  
**Output**: List of tokens

**Implementation**: `Lexer` class in `compiler.py`

**Example**:
```
Input:  var x = 10;
Output: [KEYWORD(var), IDENTIFIER(x), OPERATOR(=), NUMBER(10), SEPARATOR(;)]
```

### Phase 2: Syntax Analysis
**Purpose**: Build Abstract Syntax Tree (AST)

**Input**: List of tokens  
**Output**: AST (tree of nodes)

**Implementation**: `Parser` class using recursive descent parsing

**Example**:
```
Input:  var x = 5 + 3;
Output: VarDeclaration(name='x', value=BinaryOp('+', Number(5), Number(3)))
```

### Phase 3: Semantic Analysis
**Purpose**: Check variable declarations and types

**Input**: AST  
**Output**: Symbol table, error list

**Implementation**: `SemanticAnalyzer` class

**Features**:
- Variable declaration checking
- Undeclared variable detection
- Scope management

### Phase 4: Intermediate Code Generation
**Purpose**: Generate three-address code

**Input**: AST  
**Output**: List of three-address code instructions

**Implementation**: `IntermediateCodeGenerator` class

**Example**:
```
Input:  x = a + b * c;
Output:
  t1 = b * c
  t2 = a + t1
  x = t2
```

### Phase 5: Optimization
**Purpose**: Improve code efficiency

**Input**: Three-address code  
**Output**: Optimized three-address code

**Implementation**: `Optimizer` class

**Techniques**:
- Constant folding (e.g., `3 + 5` → `8`)
- Constant propagation
- Dead code elimination

### Phase 6: Code Generation & Execution
**Purpose**: Execute the program

**Input**: AST  
**Output**: Program output

**Implementation**: `Interpreter` class

**Features**:
- Variable storage
- Expression evaluation
- Control flow execution
- Output generation

---

## Project Structure

```
mel-compiler/
│
├── compiler.py              # Main compiler implementation
│   ├── Lexer                # Phase 1: Lexical Analysis
│   ├── Parser               # Phase 2: Syntax Analysis
│   ├── SemanticAnalyzer     # Phase 3: Semantic Analysis
│   ├── IntermediateCodeGenerator  # Phase 4: Intermediate Code
│   ├── Optimizer            # Phase 5: Optimization
│   ├── Interpreter          # Phase 6: Execution
│   └── MELCompiler          # Main compiler class
│
├── app.py                   # Streamlit web application
│
├── requirements.txt         # Python dependencies
│
├── README.md               # This file
│
│
├── test_cases/             # Test programs which are in the code
│   ├── fibonacci.mel
│   ├── factorial.mel
│   ├── sum.mel
│   ├── power.mel
│   └── even_odd.mel
│
├── handwritten_artifacts/  
│   ├── lexical_analysis.pdf
│   ├── syntax_analysis.pdf
│   ├── semantic_analysis.pdf
│   ├── intermediate_code.pdf
│   ├── optimization.pdf
│   └── execution_trace.pdf
│
└──  reflection.md
```

---

## Test Cases

### Test Case 1: Fibonacci Sequence

**Purpose**: Test loops, variables, and arithmetic

**Code**:
```mel
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

print("Done!");
```

**Expected Output**:
```
0
1
1
2
3
5
8
13
21
34
Done!
```

### Test Case 2: Factorial Calculator

**Purpose**: Test multiplication and loops

**Code**:
```mel
var n = 5;
var result = 1;
var i = 1;

while (i <= n) {
    result = result * i;
    i = i + 1;
}

print(result);
```

**Expected Output**:
```
120
```

### Test Case 3: Even/Odd Counter

**Purpose**: Test conditional statements

**Code**:
```mel
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
print(odd);
```

**Expected Output**:
```
Even:
10
Odd:
10
```

---

## Deliverables

### 1. Code Implementation ✅
- [x] Complete compiler with all 6 phases
- [x] Streamlit web interface
- [x] Test cases with expected outputs
- [x] Code annotations explaining each phase

### 2. Handwritten Artifacts ✅
- [x] DFA diagrams for lexical analysis
- [x] Parse tree examples (minimum 2)
- [x] Symbol table with scope examples
- [x] Three-address code examples
- [x] Optimization examples
- [x] Transition tables

### 3. Documentation 
- [x] Language specification (BNF grammar)
- [x] README with usage instructions
- [x] Design decisions document
- [x] Reflection (1 page)

### 4. Demonstration 
- [x] 3+ unique test cases
- [x] Working compiler execution
- [x] All phases demonstrated
- [x] Interactive web interface

---

## Design Decisions

### Why These Choices?

1. **Python**: Easy to understand, rapid development, excellent for education
2. **Streamlit**: Quick web interface without frontend complexity
3. **Recursive Descent**: Simple, intuitive parsing technique
4. **AST-based**: Clean separation between parsing and execution
5. **Three-Address Code**: Standard intermediate representation

### Trade-offs

**Advantages**:
- Easy to understand and modify
- Complete demonstration of all phases
- Interactive testing capability
- Educational clarity

**Limitations**:
- Interpreted execution (not native code)
- Limited optimization techniques
- Simple type system
- No advanced features (functions, arrays, etc.)

---

## Learning Outcomes

Through this project, we learned:

1. **Lexical Analysis**: Regular expressions, DFA construction, token recognition
2. **Parsing**: Grammar design, parse trees, recursive descent
3. **Semantic Analysis**: Symbol tables, scope management, type checking
4. **Code Generation**: Intermediate representations, three-address code
5. **Optimization**: Constant folding, dead code elimination
6. **Integration**: Combining all phases into a working compiler

---

## License

This project is created for educational purposes as part of the Compiler Construction course.


---

**Last Updated**: October 20, 2025
