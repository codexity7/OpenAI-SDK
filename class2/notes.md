## 🔸 Key Concept: `Agent`

An `Agent` is the **main component**.  
It represents a smart assistant powered by a model (like GPT-4o).  
It is highly configurable using:
- Instructions
- Tools
- Guardrails
- Handoffs
- Model Settings

---

## 🧠 Agent Properties (Explained Simply)

| Property | What it means |
|----------|----------------|
| `name` | Name of the agent (like an ID). |
| `instructions` | What the agent is told to do. Can be plain text or a function. |
| `prompt` | Dynamic way to generate instructions. |
| `handoffs` | Other agents this one can pass work to. |
| `model` | The LLM model to use (e.g. "gpt-4o"). |
| `tools` | A list of tools the agent can use. |
| `input_guardrails` | Rules to check inputs before the agent runs. |
| `output_guardrails` | Rules to check output before sending it. |
| `output_type` | Expected type of the final output (string, dict, etc). |
| `tool_use_behavior` | How the agent behaves after using a tool (see below). |
| `mcp_servers` | External tool servers (optional). |
| `reset_tool_choice` | Reset tool selection after use (default is True). |

---

## 🛠️ `tool_use_behavior` — Tool Usage Control

This setting controls what happens after a tool is used:

1. `"run_llm_again"`  
   → Run the tool, then let the LLM continue using the tool result.

2. `"stop_on_first_tool"`  
   → Stop after first tool result; don't return to LLM.

3. List of tool names  
   → If any tool in this list is used, stop and return that result.

4. Custom function  
   → You can write a function to decide if output is final or not.

---

## 🧪 Agent Functions

### `clone(...)`  
Make a copy of the agent with updated settings.  
Example:  
```python
agent.clone(instructions="New behavior")
````
### `as_tool(...)`
Turns the agent into a **tool** that other agents can call.

- Unlike handoffs, it **doesn’t transfer the conversation**.
- It behaves like a **callable function/tool**.

---

### `get_system_prompt(...)`
Returns the **system prompt** (final instruction string).

- If it's a function, it is called dynamically with context.

---

### `get_prompt(...)`
Returns a **formatted prompt** using `PromptUtil`.

---

### `get_mcp_tools(...)`
Fetches tools from **MCP servers**, if any.

---

### `get_all_tools(...)`
Returns **all tools** (agent tools + MCP tools) that are **currently active**.

---

## 📦 Data Classes & Helpers

### `ToolsToFinalOutputResult`
- A helper class to determine if the tool output should be **final**.

### `ToolsToFinalOutputFunction`
- A **custom function type** that handles tool output logic.

### `StopAtTools`
- Used to **stop the agent** if any specific tool is used.

### `MCPConfig`
- Contains **settings for MCP tool servers**.

---

## ✅ Summary

- `Agent` is the **most important class** in the SDK.
- It acts like a **smart assistant**.
- Can:
  - Use tools
  - Call sub-agents
  - Enforce input/output rules
- Highly customizable:
  - Tool behavior
  - Output formatting
  - Modular architecture

Perfect for building **smart, multi-agent AI systems**.

---



