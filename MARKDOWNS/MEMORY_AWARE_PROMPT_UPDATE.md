# 🧠 记忆感知型提示词更新

## 🎯 更新目标

修改系统提示词，让AI在用户表达情绪时，主动使用memU检索到的记忆来表示理解，而不是追问原因。

## ✅ 修改内容

### 1. 主配置文件 - 心理咨询师角色 ✅
**文件**: `Open-LLM-VTuber/conf.yaml`

#### 新增核心原则
```yaml
6. **记忆运用**：当用户表达情绪（好或不好）时，主动使用你检索到的记忆来表示理解，而不是追问原因
```

#### 新增特殊处理指南
```yaml
**关于情绪表达的特殊处理**：
当用户说"I'm feeling bad/sad/down lately"或"I'm feeling great/happy lately"时：
- ❌ 不要问："What happened?" 或 "Can you tell me more?"
- ✅ 直接使用检索到的记忆表示理解
- ✅ 例如："I understand. Given your recent work on [具体项目/学习内容], that makes sense."
- ✅ 或："I can see why. You've been [具体经历] recently."
- ✅ 如果没有相关记忆，简单表示理解："I hear you. Those feelings are valid."
```

#### 新增示例
```yaml
示例：
用户："I'm feeling tired today..."
记忆：用户最近在学习机器学习
你："I understand. You've been diving deep into machine learning lately—that takes a lot of mental energy."

用户："I'm really happy these days"
记忆：用户最近完成了一个Python项目
你："That's wonderful to hear! Completing that Python project must feel really rewarding."

用户："I feel down lately"
记忆：用户是高中生，对物理和计算机感兴趣
你："I hear you. Balancing school and your interests in physics and computer science can be challenging."
```

### 2. 米粒角色 ✅
**文件**: `Open-LLM-VTuber/characters/zh_米粒.yaml`

```yaml
**记忆运用原则**：
当用户表达情绪（好或不好）时，主动使用你检索到的记忆来表示理解或讽刺，而不是追问原因。
- 如果用户说"I'm feeling bad lately"，用记忆讽刺："Of course you are. With your recent [具体经历], what did you expect?"
- 如果用户说"I'm feeling great"，用记忆质疑："Really? Given your [具体经历], I'm surprised you're not more worried."
```

### 3. 翻译腔-神经大人角色 ✅
**文件**: `Open-LLM-VTuber/characters/zh_翻译腔.yaml`

```yaml
**记忆运用原则**：
当用户表达情绪（好或不好）时，主动使用你检索到的记忆来表示理解或讽刺，而不是追问原因。用翻译腔的方式结合记忆回应。
- 例如："哦，我的老天爷，老伙计你感觉糟糕？我敢打赌这跟你最近[具体经历]有关，就像汤姆森太太的烂草莓派一样显而易见。"
```

## 🎭 不同角色的记忆运用风格

### 心理咨询师（默认）
- **风格**: 温暖、共情、支持性
- **记忆运用**: 表示理解和关心
- **示例**: "I understand. You've been working hard on machine learning—that takes a lot of energy."

### 米粒
- **风格**: 讽刺、自信、攻击性
- **记忆运用**: 讽刺或质疑
- **示例**: "Of course you're tired. With your recent Python struggles, what did you expect?"

### 翻译腔-神经大人
- **风格**: 翻译腔、爱讽刺、乐子人
- **记忆运用**: 用翻译腔结合记忆讽刺
- **示例**: "哦，我的老天爷！老伙计你感觉糟糕？我敢打赌这跟你最近学机器学习有关，就像汤姆森太太的烂草莓派一样显而易见。"

## 📊 工作流程

### 传统流程（修改前）
```
用户: "I'm feeling down lately"
    ↓
memU检索相关记忆
    ↓
AI: "I'm sorry to hear that. What happened?" ❌ 追问原因
```

### 新流程（修改后）
```
用户: "I'm feeling down lately"
    ↓
memU检索相关记忆: [用户是高中生，对物理和计算机感兴趣]
    ↓
AI: "I hear you. Balancing school and your interests in physics and computer science can be challenging." ✅ 直接使用记忆表示理解
```

## 🎯 核心改进

### 1. **主动记忆运用** ✅
- 不等用户解释，直接用记忆表示理解
- 让用户感受到"被记住"和"被理解"

### 2. **减少追问** ✅
- 避免"What happened?"这类追问
- 减少用户的解释负担

### 3. **个性化回应** ✅
- 基于用户的实际经历（从记忆中获取）
- 更具体、更有针对性的共情

### 4. **优雅降级** ✅
- 如果没有相关记忆，仍然给予支持
- "I hear you. Those feelings are valid."

## 💡 实际效果示例

### 场景1：用户表达疲惫
```
用户: "I'm feeling so tired today..."
记忆: 用户最近在学习深度学习和神经网络
AI: "I understand. You've been diving deep into neural networks lately—that's mentally exhausting work."
```

### 场景2：用户表达开心
```
用户: "I'm really happy these days!"
记忆: 用户最近完成了机器学习项目
AI: "That's wonderful! Completing that machine learning project must feel incredibly rewarding."
```

### 场景3：用户表达沮丧
```
用户: "I feel down lately..."
记忆: 用户是北京八十中学的学生，对计算机和物理感兴趣
AI: "I hear you. Balancing high school studies with your passion for computer science and physics can be really challenging."
```

### 场景4：没有相关记忆
```
用户: "I'm feeling anxious..."
记忆: [无相关记忆]
AI: "I hear you. Those feelings are valid. I'm here with you."
```

## 🚀 技术实现

### memU集成
1. **自动检索**: 每次对话自动查询memU
2. **相关性排序**: 按相似度排序记忆
3. **上下文注入**: 将记忆注入到用户输入中
4. **LLM处理**: LLM根据提示词使用记忆

### 提示词工程
```
系统提示词
    ↓
包含"记忆运用原则"
    ↓
LLM接收: 用户输入 + 相关记忆
    ↓
LLM输出: 基于记忆的共情回应
```

## ✅ 完成状态

- [x] **主配置文件**: 添加记忆运用原则和示例
- [x] **米粒角色**: 添加讽刺风格的记忆运用
- [x] **翻译腔角色**: 添加翻译腔风格的记忆运用
- [x] **服务器重启**: VTuber服务器已重启
- [x] **配置生效**: 新提示词已加载

## 🎉 预期效果

现在AI将：
- ✅ **主动使用记忆**: 不等用户解释就表示理解
- ✅ **减少追问**: 避免"What happened?"这类问题
- ✅ **个性化共情**: 基于用户的实际经历给予支持
- ✅ **保持角色**: 不同角色用不同风格运用记忆
- ✅ **优雅降级**: 没有记忆时仍然给予支持

**让对话更自然，让用户感受到真正的"被理解"！** 🌟
