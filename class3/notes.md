
# 🧠 Running Agents in OpenAI Agents SDK

This document explains how agent execution works in detail, with diagrams and live code examples. Ideal for use as class notes or a GitHub readme.

---

## 🔄 Sync vs Async

| Type  | Method            | Description |
|-------|-------------------|-------------|
| Async | `Runner.run()`    | Asynchronous, non-blocking execution |
| Sync  | `Runner.run_sync()` | Synchronous (wraps async under the hood) |
| Async | `Runner.run_streamed()` | Asynchronous + streams events in real-time |

---

## 🔁 Agent Execution Loop

This is how agent execution works internally when using any Runner method (`run`, `run_sync`, or `run_streamed`).

### 🧠 Step-by-Step Flow:

1. **Start**  
   The loop begins when you call a Runner method with an `Agent` and an input (string or input list).

2. **Call LLM**  
   The LLM is invoked using the current agent’s configuration and input. This generates a response, which can contain:
   - A final output
   - Tool calls
   - A handoff
   - Invalid/malformed output (can raise an error)

3. **Check for Final Output**  
   If the LLM returns plain text output that:
   - Matches the agent’s `output_type`
   - Does not contain any tool calls

   ➤ Then the loop ends and the `RunResult` is returned.

4. **Check for Handoff**  
   If the LLM response contains a **handoff** to another agent:
   - The agent is switched to the new one
   - The input is updated accordingly
   - The loop restarts from Step 2 with the new agent

5. **Check for Tool Calls**  
   If tool calls are present:
   - The runner executes all tools
   - Tool outputs are appended to the message history
   - The loop restarts from Step 2 with the same agent

6. **Check Max Turns**  
   If the number of loop iterations exceeds `max_turns` (default is 10):
   - A `MaxTurnsExceeded` exception is raised
   - This prevents infinite loops

### 📌 Important Notes:

- The loop continues until one of the following occurs:
  - A valid final output is generated
  - An exception is raised
- Tool calls and handoffs can nest, meaning the loop may run through multiple agents and tools
- Only the **first agent’s input guardrails** are checked; output guardrails apply to the final response

### Steps:

1. Call LLM with current agent + input
2. If LLM returns final output → return result
3. If LLM does a handoff → switch to new agent and re-run
4. If LLM calls tools → run tool(s), add result to input, re-run
5. If max_turns is exceeded → raise `MaxTurnsExceeded`

---

## 🧪 Live Example: `Runner.run()`

```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Helper", instructions="Be helpful.")
    result = await Runner.run(agent, "Tell me a joke.")
    print(result.final_output)
```

---

## ⚙️ RunConfig Settings

You can pass `RunConfig` to customize model, tracing, guardrails etc.

```python
from agents import RunConfig

run_config = RunConfig(
    model="gpt-4",
    workflow_name="ClassWorkflow",
    trace_metadata={"user_id": "class123"}
)
```

Key Fields:
- `model`, `model_settings`
- `handoff_input_filter`
- `input_guardrails`, `output_guardrails`
- `trace_id`, `workflow_name`, `group_id`

---

## 🧵 Managing Conversations

### Manual

```python
result = await Runner.run(agent, "Where is Eiffel Tower?")
new_input = result.to_input_list() + [{"role": "user", "content": "Which country?"}]
result = await Runner.run(agent, new_input)
```

### With Sessions

```python
from agents import SQLiteSession

session = SQLiteSession("session_1")
result = await Runner.run(agent, "What's 2+2?", session=session)
result = await Runner.run(agent, "And times 3?", session=session)
```

Sessions:
- Auto-handle history
- Separate chats via session IDs

---

## 🚨 Exceptions

| Exception | Meaning |
|-----------|---------|
| `MaxTurnsExceeded` | Agent took too many turns |
| `ModelBehaviorError` | LLM returned bad output |
| `UserError` | Coding mistake in usage |
| `InputGuardrailTripwireTriggered` | Input blocked |
| `OutputGuardrailTripwireTriggered` | Output blocked |

---

## ✅ Summary

- Understand sync vs async
- How agent loop works (diagram)
- Use `run`, `run_sync`, `run_streamed`
- Pass `RunConfig` for advanced control
- Handle chats with Sessions
