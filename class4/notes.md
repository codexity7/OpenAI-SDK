# Streaming in OpenAI Agents SDK




## What is Streaming?
- **Definition:**  
  Receive live updates from an agent run instead of waiting for the full result to finish.  
- **Why it’s useful:**
  - Gives **real-time feedback** to users.
  - Allows **partial responses** to be shown as they’re generated.
  - Improves **interactivity** in apps (chat-like experiences, dashboards, etc.).
  - Reduces **perceived latency**.

---

## Key Methods

1. **`Runner.run_streamed()`**
   - Main method to start a streamed agent run.
   - Returns a `RunResultStreaming` object containing stream data and metadata.

2. **`stream_events()`**
   - Async generator that **yields events** as they happen.
   - Can be used to process events one-by-one in real time.



---

## Types of Streamed Events

All streamed events are subclasses of `StreamedEvent`.

---

### 1. Raw Response Streamed Events
- **Purpose:** Low-level streaming data directly from the LLM.
- **Typical granularity:** Token-by-token updates.
- **Example:**
  - **`ResponseTextDeltaEvent`** → gives incremental text (delta) from the LLM.

---

### 2. Run Item Streamed Events
- **Purpose:** High-level agent actions during the run.
- **Examples:**
  - **`messageOutputItem`** → Full message from the LLM is ready.
  - **`toolCallItem`** → Agent invoked a tool.
  - **`toolCallOutputItem`** → Tool finished and returned a value.
- **Note:** These events are more structured than raw text deltas.

---

### 3. Agent Handoff Events
- **Purpose:** Indicates when control passes to a **different agent** in the same run.
- **Example:**  
  - `agent_updated_stream_events` → may signify a handoff to another agent.

---

## Event Handling Tips
- **Check event types** using `isinstance(event.data, ResponseTextDeltaEvent)` or other event classes.
- **Combine deltas** for final text output if needed.
- **Use try/except** inside `stream_events()` loops to avoid breaking on unexpected event types.

---

## Common Use Cases
- Live chat applications.
- Real-time analytics dashboards.
- Progressive content rendering (e.g., document generation).
- Tool-assisted conversations where results are shown as they arrive.
