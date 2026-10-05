#11420340莊佳臻
#11420345魏宇嫻
import re

# 定義運算子優先順序與結合性
# 次方 (^) 為右結合 (Right-associative)，其餘為左結合 (Left-associative)
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}

def tokenize(expression: str) -> list[str]:
    """將輸入字串切分為運算元（數字）與運算子標記（Tokens）。"""
    # 支援整數、小數點數字，以及 + - * / ^ ( )
    pattern = r'\d+(?:\.\d+)?|[+\-*/^()]'
    return re.findall(pattern, expression)

def infix_to_postfix(tokens: list[str]) -> list[str]:
    """使用 Shunting-yard 演算法將中序式轉換為後序式。"""
    output = []
    op_stack = []

    for token in tokens:
        # 1. 若為數字（運算元），直接加入輸出
        if re.match(r'^\d+(?:\.\d+)?$', token):
            output.append(token)
            
        # 2. 若為左括號，推入堆疊
        elif token == '(':
            op_stack.append(token)
            
        # 3. 若為右括號，將堆疊中的運算子依序彈出直到遇到左括號
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output.append(op_stack.pop())
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()  # 彈出 '('
            else:
                raise ValueError("括號不對稱")
                
        # 4. 若為運算子 (+, -, *, /, ^)
        elif token in PRECEDENCE:
            current_prec = PRECEDENCE[token]
            while op_stack and op_stack[-1] != '(':
                top_op = op_stack[-1]
                top_prec = PRECEDENCE.get(top_op, 0)
                
                # 次方 (^) 是右結合：僅當堆疊頂端優先權嚴格大於當前運算子時才彈出
                # 左結合運算子：堆疊頂端優先權大於或等於當前運算子時即彈出
                if token == '^':
                    if top_prec > current_prec:
                        output.append(op_stack.pop())
                    else:
                        break
                else:
                    if top_prec >= current_prec:
                        output.append(op_stack.pop())
                    else:
                        break
            op_stack.append(token)

    # 將堆疊中剩餘的運算子彈出
    while op_stack:
        top = op_stack.pop()
        if top in ('(', ')'):
            raise ValueError("括號不對稱")
        output.append(top)

    return output

def evaluate_postfix(postfix_tokens: list[str]) -> float:
    """計算後序運算式的值。"""
    val_stack = []

    for token in postfix_tokens:
        # 若為數字，轉為 float 後推入堆疊
        if re.match(r'^\d+(?:\.\d+)?$', token):
            val_stack.append(float(token))
        elif token in PRECEDENCE:
            if len(val_stack) < 2:
                raise ValueError("運算式無效，缺少運算元")
            b = val_stack.pop()
            a = val_stack.pop()

            if token == '+':
                val_stack.append(a + b)
            elif token == '-':
                val_stack.append(a - b)
            elif token == '*':
                val_stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("除數不可為 0")
                val_stack.append(a / b)
            elif token == '^':
                val_stack.append(a ** b)

    if len(val_stack) != 1:
        raise ValueError("運算式無效，運算子與運算元數量不符")

    return val_stack[0]

def process_expression(expr: str):
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix)
    
    # 格式化輸出數值（若為整數則去除小數點）
    formatted_result = int(result) if result.is_integer() else result
    
    print(f"中序式 (Infix)   : {expr}")
    print(f"後序式 (Postfix) : {' '.join(postfix)}")
    print(f"運算結果         : {formatted_result}")
    print("-" * 40)

# --- 測試與互動執行 ---
if __name__ == "__main__":
    # 執行題目指定的測試案例
    print("=== 預設測試案例 ===")
    test_cases = [
        "(6 + 4) * 5",
        "(56 + 12) * 3 - 4",
        "2 ^ 3 ^ 2"  # 測試次方右結合性：2^(3^2) = 2^9 = 512
    ]
    
    for case in test_cases:
        process_expression(case)

    # 允許使用者自訂輸入
    while True:
        print("=== 自訂輸入 (輸入 'exit' 或 'q' 結束) ===")
        try:
            user_input = input("請輸入中序式: ").strip()
            if user_input.lower() in ('exit', 'q', ''):
                break
            process_expression(user_input)
        except Exception as e:
            print(f"錯誤: {e}")