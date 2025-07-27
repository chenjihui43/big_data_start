import re
from collections import OrderedDict

# 文档集内容
corpus = """
"State-of-the-art named entity recognition systems rely heavily on hand-crafted features and domain-specific knowledge in order to learn effectively from the small",
"supervised training corpora that are available. In this paper, we introduce two new neural architectures: one based on bidirectional LSTMs and conditional random fields",
"and the other that constructs and labels segments using a transition-based approach inspired by shift-reduce parsers. Our models rely on two sources of information about words", 
"character-based word representations learned from the supervised corpus and unsupervised word representations learned from unannotated corpora",
"Our models obtain state-of-the-art performance in NER in four languages without resorting to any language-specific knowledge or resources such as gazetteers"
"""

# 1. 将文档集内容写入文件
with open('input.txt', 'w', encoding='utf-8') as f:
    f.write(corpus.strip())

# 2. 从文件读取所有句子
sentences = []
with open('input.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # 去除首尾空白字符和引号
        line = line.strip().strip(',')
        line = line.strip().strip('"')
        if line:
            sentences.append(line)

print(sentences)

# 3. 统计所有词（构建词汇表）
word_set = set()
for sentence in sentences:
    # 使用正则表达式分词：匹配单词（允许连字符和撇号）
    words = re.findall(r"\b[\w'-]+\b", sentence.lower())
    word_set.update(words)

# 创建有序词汇表（按字母顺序排序）
vocab = OrderedDict(sorted({word: idx for idx, word in enumerate(sorted(word_set))}.items()))

# 4. 为每个句子创建词袋向量
vectors = []
for sentence in sentences:
    # 初始化全零向量
    vector = [0] * len(vocab)
    words = re.findall(r"\b[\w'-]+\b", sentence.lower())
    for word in words:
        if word in vocab:
            # 增加对应单词的计数
            vector[vocab[word]] += 1
    vectors.append(vector)

# 5. 将向量保存到新文档
with open('output_vectors.txt', 'w', encoding='utf-8') as f:
    for i, vector in enumerate(vectors):
        # 将向量转换为逗号分隔的字符串
        vec_str = ','.join(map(str, vector))
        f.write(f"Sentence {i + 1}: {vec_str}\n")
