"""
MEL Compiler - Mathematical Expression Language
Complete 6-Phase Compiler Implementation
"""

import re
from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# ============================================================================
# PHASE 1: LEXICAL ANALYSIS
# ============================================================================

class TokenType(Enum):
    """Token types for MEL language"""
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    SEPARATOR = "SEPARATOR"
    COMMENT = "COMMENT"
    EOF = "EOF"

@dataclass
class Token:
    """Token representation"""
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    """Lexical Analyzer - Phase 1"""
    
    KEYWORDS = {'var', 'if', 'else', 'while', 'for', 'print', 'function', 'return'}
    OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!'}
    SEPARATORS = {'(', ')', '{', '}', ';', ','}
    
    def __init__(self, source_code: str):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def tokenize(self) -> List[Token]:
        """Perform lexical analysis and return list of tokens"""
        while self.position < len(self.source):
            self._skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            char = self.source[self.position]
            
            # Comments
            if char == '#':
                self._read_comment()
            # String literals
            elif char == '"':
                self._read_string()
            # Numbers
            elif char.isdigit():
                self._read_number()
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self._read_identifier()
            # Operators
            elif self._is_operator_start(char):
                self._read_operator()
            # Separators
            elif char in self.SEPARATORS:
                self._read_separator()
            else:
                self._advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _skip_whitespace(self):
        """Skip whitespace characters"""
        while self.position < len(self.source) and self.source[self.position].isspace():
            if self.source[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1
    
    def _read_comment(self):
        """Read comment token"""
        start_col = self.column
        comment = ''
        while self.position < len(self.source) and self.source[self.position] != '\n':
            comment += self.source[self.position]
            self._advance()
        self.tokens.append(Token(TokenType.COMMENT, comment, self.line, start_col))
    
    def _read_string(self):
        """Read string literal"""
        start_col = self.column
        self._advance()  # Skip opening quote
        value = ''
        while self.position < len(self.source) and self.source[self.position] != '"':
            value += self.source[self.position]
            self._advance()
        self._advance()  # Skip closing quote
        self.tokens.append(Token(TokenType.STRING, value, self.line, start_col))
    
    def _read_number(self):
        """Read numeric literal"""
        start_col = self.column
        value = ''
        while self.position < len(self.source) and (self.source[self.position].isdigit() or self.source[self.position] == '.'):
            value += self.source[self.position]
            self._advance()
        self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_col))
    
    def _read_identifier(self):
        """Read identifier or keyword"""
        start_col = self.column
        value = ''
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            value += self.source[self.position]
            self._advance()
        
        token_type = TokenType.KEYWORD if value in self.KEYWORDS else TokenType.IDENTIFIER
        self.tokens.append(Token(token_type, value, self.line, start_col))
    
    def _is_operator_start(self, char: str) -> bool:
        """Check if character can start an operator"""
        return char in {'+', '-', '*', '/', '=', '!', '<', '>', '&', '|'}
    
    def _read_operator(self):
        """Read operator token"""
        start_col = self.column
        value = self.source[self.position]
        self._advance()
        
        # Check for two-character operators
        if self.position < len(self.source):
            two_char = value + self.source[self.position]
            if two_char in self.OPERATORS:
                value = two_char
                self._advance()
        
        self.tokens.append(Token(TokenType.OPERATOR, value, self.line, start_col))
    
    def _read_separator(self):
        """Read separator token"""
        start_col = self.column
        value = self.source[self.position]
        self._advance()
        self.tokens.append(Token(TokenType.SEPARATOR, value, self.line, start_col))
    
    def _advance(self):
        """Move to next character"""
        self.position += 1
        self.column += 1

# ============================================================================
# PHASE 2: SYNTAX ANALYSIS
# ============================================================================

@dataclass
class ASTNode:
    """Base class for AST nodes"""
    type: str

@dataclass
class VarDeclaration(ASTNode):
    name: str
    value: Any

@dataclass
class Assignment(ASTNode):
    name: str
    value: Any

@dataclass
class WhileLoop(ASTNode):
    condition: Any
    body: List[ASTNode]

@dataclass
class IfStatement(ASTNode):
    condition: Any
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

@dataclass
class PrintStatement(ASTNode):
    value: Any

@dataclass
class BinaryOp(ASTNode):
    operator: str
    left: Any
    right: Any

@dataclass
class Number(ASTNode):
    value: float

@dataclass
class String(ASTNode):
    value: str

@dataclass
class Identifier(ASTNode):
    name: str

class Parser:
    """Syntax Analyzer - Phase 2"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type != TokenType.COMMENT]
        self.current = 0
        self.ast = []
    
    def parse(self) -> List[ASTNode]:
        """Parse tokens and build AST"""
        while self.current < len(self.tokens) and self.tokens[self.current].type != TokenType.EOF:
            stmt = self._statement()
            if stmt:
                self.ast.append(stmt)
        return self.ast
    
    def _statement(self) -> Optional[ASTNode]:
        """Parse a statement"""
        if self._check('var'):
            return self._var_declaration()
        elif self._check('while'):
            return self._while_loop()
        elif self._check('if'):
            return self._if_statement()
        elif self._check('print'):
            return self._print_statement()
        elif self._peek().type == TokenType.IDENTIFIER:
            return self._assignment()
        else:
            self._advance()
            return None
    
    def _var_declaration(self) -> VarDeclaration:
        """Parse variable declaration"""
        self._consume('var')
        name = self._consume_identifier()
        self._consume('=')
        value = self._expression()
        self._consume(';')
        return VarDeclaration('VarDeclaration', name, value)
    
    def _assignment(self) -> Assignment:
        """Parse assignment statement"""
        name = self._consume_identifier()
        self._consume('=')
        value = self._expression()
        self._consume(';')
        return Assignment('Assignment', name, value)
    
    def _while_loop(self) -> WhileLoop:
        """Parse while loop"""
        self._consume('while')
        self._consume('(')
        condition = self._expression()
        self._consume(')')
        self._consume('{')
        body = []
        while not self._check('}'):
            stmt = self._statement()
            if stmt:
                body.append(stmt)
        self._consume('}')
        return WhileLoop('WhileLoop', condition, body)
    
    def _if_statement(self) -> IfStatement:
        """Parse if statement"""
        self._consume('if')
        self._consume('(')
        condition = self._expression()
        self._consume(')')
        self._consume('{')
        then_branch = []
        while not self._check('}'):
            stmt = self._statement()
            if stmt:
                then_branch.append(stmt)
        self._consume('}')
        
        else_branch = None
        if self._check('else'):
            self._consume('else')
            self._consume('{')
            else_branch = []
            while not self._check('}'):
                stmt = self._statement()
                if stmt:
                    else_branch.append(stmt)
            self._consume('}')
        
        return IfStatement('IfStatement', condition, then_branch, else_branch)
    
    def _print_statement(self) -> PrintStatement:
        """Parse print statement"""
        self._consume('print')
        self._consume('(')
        value = self._expression()
        self._consume(')')
        self._consume(';')
        return PrintStatement('Print', value)
    
    def _expression(self) -> Any:
        """Parse expression"""
        return self._logical_or()
    
    def _logical_or(self) -> Any:
        """Parse logical OR expression"""
        left = self._logical_and()
        while self._check('||'):
            op = self._advance().value
            right = self._logical_and()
            left = BinaryOp('BinaryOp', op, left, right)
        return left
    
    def _logical_and(self) -> Any:
        """Parse logical AND expression"""
        left = self._equality()
        while self._check('&&'):
            op = self._advance().value
            right = self._equality()
            left = BinaryOp('BinaryOp', op, left, right)
        return left
    
    def _equality(self) -> Any:
        """Parse equality expression"""
        left = self._comparison()
        while self._check_any(['==', '!=']):
            op = self._advance().value
            right = self._comparison()
            left = BinaryOp('BinaryOp', op, left, right)
        return left
    
    def _comparison(self) -> Any:
        """Parse comparison expression"""
        left = self._additive()
        while self._check_any(['<', '>', '<=', '>=']):
            op = self._advance().value
            right = self._additive()
            left = BinaryOp('BinaryOp', op, left, right)
        return left
    
    def _additive(self) -> Any:
        """Parse additive expression"""
        left = self._multiplicative()
        while self._check_any(['+', '-']):
            op = self._advance().value
            right = self._multiplicative()
            left = BinaryOp('BinaryOp', op, left, right)
        return left
    
    def _multiplicative(self) -> Any:
        """Parse multiplicative expression"""
        left = self._primary()
        while self._check_any(['*', '/']):
            op = self._advance().value
            right = self._primary()
            left = BinaryOp('BinaryOp', op, left, right)
        return left
    
    def _primary(self) -> Any:
        """Parse primary expression"""
        token = self._peek()
        
        if token.type == TokenType.NUMBER:
            self._advance()
            return Number('Number', float(token.value))
        elif token.type == TokenType.STRING:
            self._advance()
            return String('String', token.value)
        elif token.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier('Identifier', token.value)
        elif self._check('('):
            self._consume('(')
            expr = self._expression()
            self._consume(')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token.value}")
    
    def _check(self, value: str) -> bool:
        """Check if current token matches value"""
        return self._peek().value == value
    
    def _check_any(self, values: List[str]) -> bool:
        """Check if current token matches any value"""
        return self._peek().value in values
    
    def _peek(self) -> Token:
        """Get current token without consuming"""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return Token(TokenType.EOF, '', 0, 0)
    
    def _advance(self) -> Token:
        """Consume and return current token"""
        token = self._peek()
        self.current += 1
        return token
    
    def _consume(self, expected: str):
        """Consume token with expected value"""
        token = self._peek()
        if token.value != expected:
            raise SyntaxError(f"Expected '{expected}', got '{token.value}'")
        self._advance()
    
    def _consume_identifier(self) -> str:
        """Consume and return identifier"""
        token = self._peek()
        if token.type != TokenType.IDENTIFIER:
            raise SyntaxError(f"Expected identifier, got '{token.value}'")
        self._advance()
        return token.value

# ============================================================================
# PHASE 3: SEMANTIC ANALYSIS
# ============================================================================

@dataclass
class Symbol:
    """Symbol table entry"""
    name: str
    type: str
    scope: str
    line: int
    declared: bool = True
    error: Optional[str] = None

class SemanticAnalyzer:
    """Semantic Analyzer - Phase 3"""
    
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.symbol_list: List[Symbol] = []
        self.errors: List[str] = []
        self.current_scope = 'global'
    
    def analyze(self, ast: List[ASTNode]) -> List[Symbol]:
        """Perform semantic analysis"""
        for node in ast:
            self._analyze_node(node)
        return self.symbol_list
    
    def _analyze_node(self, node: ASTNode):
        """Analyze a single AST node"""
        if isinstance(node, VarDeclaration):
            if node.name in self.symbols:
                self.errors.append(f"Variable '{node.name}' already declared")
                self.symbol_list.append(Symbol(
                    node.name, 'variable', self.current_scope, 0, True, 'Already declared'
                ))
            else:
                self.symbols[node.name] = Symbol(
                    node.name, 'variable', self.current_scope, 0, True
                )
                self.symbol_list.append(self.symbols[node.name])
        
        elif isinstance(node, Assignment):
            if node.name not in self.symbols:
                self.errors.append(f"Variable '{node.name}' not declared")
                self.symbol_list.append(Symbol(
                    node.name, 'error', self.current_scope, 0, False, 'Undeclared variable'
                ))
        
        elif isinstance(node, (WhileLoop, IfStatement)):
            if isinstance(node, WhileLoop):
                for stmt in node.body:
                    self._analyze_node(stmt)
            else:
                for stmt in node.then_branch:
                    self._analyze_node(stmt)
                if node.else_branch:
                    for stmt in node.else_branch:
                        self._analyze_node(stmt)

# ============================================================================
# PHASE 4: INTERMEDIATE CODE GENERATION
# ============================================================================

class IntermediateCodeGenerator:
    """Intermediate Code Generator - Phase 4 (Three-Address Code)"""
    
    def __init__(self):
        self.code: List[str] = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def generate(self, ast: List[ASTNode]) -> List[str]:
        """Generate three-address code"""
        for node in ast:
            self._generate_node(node)
        return self.code
    
    def _new_temp(self) -> str:
        """Generate new temporary variable"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def _new_label(self) -> str:
        """Generate new label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def _generate_node(self, node: ASTNode):
        """Generate code for AST node"""
        if isinstance(node, VarDeclaration):
            temp = self._generate_expr(node.value)
            self.code.append(f"{node.name} = {temp}")
        
        elif isinstance(node, Assignment):
            temp = self._generate_expr(node.value)
            self.code.append(f"{node.name} = {temp}")
        
        elif isinstance(node, WhileLoop):
            start_label = self._new_label()
            end_label = self._new_label()
            self.code.append(f"{start_label}:")
            cond_temp = self._generate_expr(node.condition)
            self.code.append(f"if {cond_temp} == 0 goto {end_label}")
            for stmt in node.body:
                self._generate_node(stmt)
            self.code.append(f"goto {start_label}")
            self.code.append(f"{end_label}:")
        
        elif isinstance(node, IfStatement):
            else_label = self._new_label()
            end_label = self._new_label()
            cond_temp = self._generate_expr(node.condition)
            self.code.append(f"if {cond_temp} == 0 goto {else_label}")
            for stmt in node.then_branch:
                self._generate_node(stmt)
            self.code.append(f"goto {end_label}")
            self.code.append(f"{else_label}:")
            if node.else_branch:
                for stmt in node.else_branch:
                    self._generate_node(stmt)
            self.code.append(f"{end_label}:")
        
        elif isinstance(node, PrintStatement):
            temp = self._generate_expr(node.value)
            self.code.append(f"print {temp}")
    
    def _generate_expr(self, node: Any) -> str:
        """Generate code for expression"""
        if isinstance(node, Number):
            return str(node.value)
        elif isinstance(node, String):
            return f'"{node.value}"'
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, BinaryOp):
            left = self._generate_expr(node.left)
            right = self._generate_expr(node.right)
            temp = self._new_temp()
            self.code.append(f"{temp} = {left} {node.operator} {right}")
            return temp
        return "unknown"

# ============================================================================
# PHASE 5: OPTIMIZATION
# ============================================================================

class Optimizer:
    """Code Optimizer - Phase 5"""
    
    @staticmethod
    def optimize(tac: List[str]) -> List[str]:
        """Perform basic optimizations"""
        optimized = []
        constants = {}
        
        for line in tac:
            # Constant folding
            match = re.match(r'(\w+) = ([\d.]+) ([+\-*/]) ([\d.]+)', line)
            if match:
                result, left, op, right = match.groups()
                left_val = float(left)
                right_val = float(right)
                
                if op == '+':
                    value = left_val + right_val
                elif op == '-':
                    value = left_val - right_val
                elif op == '*':
                    value = left_val * right_val
                elif op == '/':
                    value = left_val / right_val if right_val != 0 else 0
                else:
                    value = 0
                
                constants[result] = value
                optimized.append(f"{result} = {value}  # Constant folded")
            
            # Constant propagation
            elif any(const in line for const in constants):
                new_line = line
                for const, value in constants.items():
                    new_line = new_line.replace(const, str(value))
                optimized.append(new_line)
            
            else:
                optimized.append(line)
        
        return optimized

# ============================================================================
# PHASE 6: CODE GENERATION & EXECUTION
# ============================================================================

class Interpreter:
    """Code Generator & Executor - Phase 6"""
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.output: List[str] = []
    
    def execute(self, ast: List[ASTNode]) -> str:
        """Execute AST and return output"""
        for node in ast:
            self._execute_node(node)
        return '\n'.join(self.output)
    
    def _execute_node(self, node: ASTNode):
        """Execute a single AST node"""
        if isinstance(node, VarDeclaration):
            self.variables[node.name] = self._evaluate_expr(node.value)
        
        elif isinstance(node, Assignment):
            self.variables[node.name] = self._evaluate_expr(node.value)
        
        elif isinstance(node, WhileLoop):
            while self._evaluate_expr(node.condition):
                for stmt in node.body:
                    self._execute_node(stmt)
        
        elif isinstance(node, IfStatement):
            if self._evaluate_expr(node.condition):
                for stmt in node.then_branch:
                    self._execute_node(stmt)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self._execute_node(stmt)
        
        elif isinstance(node, PrintStatement):
            value = self._evaluate_expr(node.value)
            self.output.append(str(value))
    
    def _evaluate_expr(self, node: Any) -> Any:
        """Evaluate expression"""
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Identifier):
            return self.variables.get(node.name, 0)
        elif isinstance(node, BinaryOp):
            left = self._evaluate_expr(node.left)
            right = self._evaluate_expr(node.right)
            
            if node.operator == '+':
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                return left / right if right != 0 else 0
            elif node.operator == '<':
                return 1 if left < right else 0
            elif node.operator == '>':
                return 1 if left > right else 0
            elif node.operator == '<=':
                return 1 if left <= right else 0
            elif node.operator == '>=':
                return 1 if left >= right else 0
            elif node.operator == '==':
                return 1 if left == right else 0
            elif node.operator == '!=':
                return 1 if left != right else 0
            elif node.operator == '&&':
                return 1 if left and right else 0
            elif node.operator == '||':
                return 1 if left or right else 0
        
        return 0

# ============================================================================
# MAIN COMPILER CLASS
# ============================================================================

class MELCompiler:
    """Main compiler class integrating all phases"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens = []
        self.ast = []
        self.symbols = []
        self.intermediate_code = []
        self.optimized_code = []
        self.output = ""
    
    def compile_and_run(self) -> Dict[str, Any]:
        """Run all compilation phases"""
        try:
            # Phase 1: Lexical Analysis
            lexer = Lexer(self.source_code)
            self.tokens = lexer.tokenize()
            
            # Phase 2: Syntax Analysis
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            
            # Phase 3: Semantic Analysis
            semantic_analyzer = SemanticAnalyzer()
            self.symbols = semantic_analyzer.analyze(self.ast)
            
            # Phase 4: Intermediate Code Generation
            ic_generator = IntermediateCodeGenerator()
            self.intermediate_code = ic_generator.generate(self.ast)
            
            # Phase 5: Optimization
            self.optimized_code = Optimizer.optimize(self.intermediate_code)
            
            # Phase 6: Execution
            interpreter = Interpreter()
            self.output = interpreter.execute(self.ast)
            
            return {
                'success': True,
                'tokens': self.tokens,
                'ast': self.ast,
                'symbols': self.symbols,
                'intermediate_code': self.intermediate_code,
                'optimized_code': self.optimized_code,
                'output': self.output,
                'errors': semantic_analyzer.errors
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': f"Compilation Error: {str(e)}"
            }

# ============================================================================
# TEST EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Fibonacci
    fibonacci_code = """
# Fibonacci sequence generator
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
"""
    
    print("=" * 80)
    print("MEL COMPILER - Example 1: Fibonacci")
    print("=" * 80)
    
    compiler = MELCompiler(fibonacci_code)
    result = compiler.compile_and_run()
    
    if result['success']:
        print("\n[PHASE 1: LEXICAL ANALYSIS]")
        print(f"Tokens generated: {len(result['tokens'])}")
        
        print("\n[PHASE 2: SYNTAX ANALYSIS]")
        print(f"AST nodes: {len(result['ast'])}")
        
        print("\n[PHASE 3: SEMANTIC ANALYSIS]")
        print(f"Symbols in table: {len(result['symbols'])}")
        
        print("\n[PHASE 4: INTERMEDIATE CODE]")
        for line in result['intermediate_code'][:10]:
            print(f"  {line}")
        
        print("\n[PHASE 5: OPTIMIZED CODE]")
        for line in result['optimized_code'][:10]:
            print(f"  {line}")
        
        print("\n[PHASE 6: EXECUTION OUTPUT]")
        print(result['output'])
    else:
        print(f"\nError: {result['error']}")