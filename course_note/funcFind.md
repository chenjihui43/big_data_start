
`str.find()` 是 Python 中用于字符串查找的常用方法，其功能是**在字符串中查找指定子字符串首次出现的位置索引**。如果未找到，则返回 `-1`。该方法常用于判断子字符串是否存在、定位子字符串位置或进行字符串切片等操作。

---

### **基本语法**
```python
str.find(sub, start=0, end=len(str))
```

- **`sub`**：要查找的子字符串（必须为字符串类型）。
- **`start`（可选）**：开始查找的起始索引（默认为 `0`）。
- **`end`（可选）**：结束查找的结束索引（默认为字符串长度 `len(str)`，不包含该索引位置的字符）。

---

### **功能详解**

#### **1. 基本查找**
- 返回子字符串 `sub` 首次出现的起始索引。
- 如果未找到，返回 `-1`。
- 查找是**区分大小写**的。

```python
s = "Hello, World!"
print(s.find("World"))  # 输出: 7
print(s.find("world"))  # 输出: -1（未找到）
```

#### **2. 指定查找范围（`start` 和 `end` 参数）**
- 可在字符串的子区间内查找。
- `start` 和 `end` 支持负数索引（从右往左数）。

```python
s = "Python is powerful and Python is fun!"
print(s.find("Python", 5))  # 从索引5开始查找，输出: 23
print(s.find("Python", 0, 10))  # 在索引0~10范围内查找，输出: 0
```

#### **3. 查找多字符子串**
- 支持查找多个字符组成的子串。

```python
s = "banana"
print(s.find("ana"))  # 输出: 1（"ana"首次出现在索引1）
```

---

### **与 `str.index()` 的区别**
- `str.find()` 和 `str.index()` 功能相似，但行为不同：
  - `find()`：未找到时返回 `-1`。
  - `index()`：未找到时抛出 `ValueError` 异常。

```python
s = "Hello, World!"
print(s.find("Java"))  # 输出: -1
try:
    print(s.index("Java"))  # 抛出异常
except ValueError as e:
    print(e)  # 输出: substring not found
```

---

### **常见用法**

#### **1. 判断子字符串是否存在**
```python
s = "Hello, World!"
if s.find("World") != -1:
    print("子字符串存在")
```

#### **2. 定位子字符串位置**
```python
s = "The quick brown fox jumps over the lazy dog."
pos = s.find("fox")
print(f"子字符串在索引 {pos} 开始")  # 输出: 子字符串在索引 16 开始
```

#### **3. 提取子字符串**
- 结合切片操作提取目标内容。

```python
s = "https://example.com/path/to/file.txt"
start = s.find("//") + 2
end = s.find("/", start)
domain = s[start:end]
print(domain)  # 输出: example.com
```

#### **4. 查找所有匹配位置**
- 循环调用 `find()` 查找所有出现的位置。

```python
s = "abracadabra"
sub = "a"
positions = []
start = 0
while True:
    pos = s.find(sub, start)
    if pos == -1:
        break
    positions.append(pos)
    start = pos + 1
print(positions)  # 输出: [0, 3, 5, 7, 10]
```

---

### **注意事项**

1. **大小写敏感**
   - 区分大小写，需注意匹配规则。
   ```python
   s = "Hello"
   print(s.find("h"))  # 输出: -1
   ```

2. **参数类型限制**
   - `sub` 必须是字符串类型，否则抛出 `TypeError`。
   ```python
   try:
       "abc".find(123)  # 错误：参数不是字符串
   except TypeError as e:
       print(e)  # 输出: must be str, not int
   ```

3. **负数索引处理**
   - `start` 和 `end` 支持负数，表示从字符串末尾倒数。
   ```python
   s = "Python"
   print(s.find("y", -3))  # 从倒数第3个字符开始查找，输出: 4
   ```

4. **空字符串的处理**
   - 查找空字符串时，返回 `0`（空字符串被视为存在于任何位置）。
   ```python
   print("abc".find(""))  # 输出: 0
   ```

---

### **与正则表达式的对比**
- `str.find()` 仅支持固定子字符串查找。
- 若需匹配复杂模式（如正则表达式），使用 `re` 模块。

```python
import re
s = "The price is $100."
match = re.search(r"\$\d+", s)
if match:
    print(match.start())  # 输出: 12（匹配 "$100" 的起始位置）
```

---

### **总结**
- `str.find()` 是定位子字符串位置的基础工具，适用于简单查找场景。
- 通过 `start` 和 `end` 参数可灵活控制查找范围。
- 未找到时返回 `-1`，适合需要避免异常的场景。
- 常用于字符串解析、数据提取、条件判断等任务。