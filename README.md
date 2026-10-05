# 中序式轉後序式與求值程式 (Infix to Postfix Converter & Evaluator)

本專案使用 Python 實作 **Shunting-yard 演算法**，支援中序式轉後序式（逆波蘭表示法，RPN），並利用堆疊（Stack）計算其運算結果。

## 支援功能

* **支援五大運算子**：
  * 加法 (`+`)、減法 (`-`)：優先級 1，左結合
  * 乘法 (`*`)、除法 (`/`)：優先級 2，左結合
  * 次方 (`^`)：優先級 3，**右結合**（例如：`2 ^ 3 ^ 2` 等同於 `2 ^ (3 ^ 2) = 512`）
* **支援括號運算**：`(` 與 `)`
* **支援多位數與小數運算**

## Python 原始碼

```python
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
    pattern = r'\d+(?:\.\d+)?|[+\-*/^()]'
    return re.findall(pattern, expression)

def infix_to_postfix(tokens: list[str]) -> list[str]:
    """使用 Shunting-yard 演算法將中序式轉換為後序式。"""
    output = []
    op_stack = []

    for token in tokens:
        # 1. 若為數字（運算元），直接加入輸出佇列
        if re.match(r'^\d+(?:\.\d+)?$', token):
            output.append(token)
            
        # 2. 若為左括號，推入運算子堆疊
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
                
                # 次方 (^) 為右結合：堆疊頂端優先權嚴格大於當前運算子才彈出
                # 左結合運算子：堆疊頂端優先權大於或等於當前運算子即彈出
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
        # 數字轉為 float 後推入數值堆疊
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
    """處理並輸出結果"""
    tokens = tokenize(expr)
    postfix = infix_to_postfix(tokens)
    result = evaluate_postfix(postfix)
    
    # 格式化輸出數值（若為整數則轉為 int 呈現）
    formatted_result = int(result) if result.is_integer() else result
    
    print(f"中序式 (Infix)   : {expr}")
    print(f"後序式 (Postfix) : {' '.join(postfix)}")
    print(f"運算結果         : {formatted_result}")
    print("-" * 40)

if __name__ == "__main__":
    # 指定測試案例
    print("=== 測試案例執行 ===")
    test_cases = [
        "(6 + 4) * 5",
        "(56 + 12) * 3 - 4",
        "2 ^ 3 ^ 2"
    ]
    
    for case in test_cases:
        process_expression(case)

    # 互動式輸入
    print("=== 互動輸入測試 (輸入 'q' 結束) ===")
    while True:
        try:
            user_input = input("請輸入中序式: ").strip()
            if user_input.lower() in ('exit', 'q', ''):
                break
            process_expression(user_input)
        except Exception as e:
            print(f"錯誤: {e}")
```

## 測試案例與輸出說明

| 測試案例 | 後序式 (Postfix) | 計算步驟 | 運算結果 |
| :--- | :--- | :--- | :--- |
| `(6 + 4) * 5` | `6 4 + 5 *` | `(6 + 4) * 5 = 10 * 5` | `50` |
| `(56 + 12) * 3 - 4` | `56 12 + 3 * 4 -` | `(56 + 12) * 3 - 4 = 68 * 3 - 4 = 204 - 4` | `200` |
| `2 ^ 3 ^ 2` | `2 3 2 ^ ^` | `2 ^ (3 ^ 2) = 2 ^ 9` | `512` |
