# How to Run Queue Tasks Sequentially with GNHF

This document explains how to sequentially execute the structured research tasks defined in [docs/antigravity_queue/](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/docs/antigravity_queue/) one at a time using **gnhf** ("good night, have fun") and Claude.

## 1. Rationale & Approach

- **Sequential Execution**: Running tasks one by one prevents race conditions and makes it simple to inspect the git commits, debug logs, and output reports for each task before moving on.
- **Incremental commits**: Each task is executed inside `gnhf`, which automatically commits successful iterations, checkpoints progress, and isolates changes.
- **Verification-Gated**: Each task utilizes the `/research-cycle` workflow, which runs the full Plan → Execute → Verify → Wrap-up loop. The final validation must pass the `auditor` gate.
- **Skip Completed Tasks**: The runner checks if a report file already exists in [docs/antigravity_queue/reports/](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/docs/antigravity_queue/reports/) for each task. Completed tasks are skipped automatically.

---

## 2. Configuration (Specifying Claude Haiku 4.5)

To specify that `gnhf` should use the Claude Haiku 4.5 model, configure the global `~/.gnhf/config.yml` file.

1. Open or create `~/.gnhf/config.yml`.
2. Add/modify the `agent` and `agentArgsOverride` fields as follows:

```yaml
agent: claude

agentArgsOverride:
  claude:
    - --model
    - claude-haiku-4-5-20251001
```

---

## 3. How to Run the Queue

Execute the following steps from the root of your project directory (`CABP_copy_for_antigravity`):

1. **Switch to your base branch** (mandatory before using worktrees):
   ```bash
   git checkout antigravity
   ```

2. **Clean up any lingering background processes** to avoid session lock errors:
   ```bash
   pkill -f pytest
   pkill -f /versions/
   ```

3. **Run the sequential loop** (uses a single-line command prompt and a `sleep 5` safety buffer):
   ```bash
   for task_file in docs/antigravity_queue/task_*.md; do
     task_name=$(basename "$task_file" .md)
     task_letter=$(echo "$task_name" | cut -d'_' -f2 | tr '[:upper:]' '[:lower:]')
     report_file="docs/antigravity_queue/reports/task_${task_letter}_report.md"
     
     if [ -f "$report_file" ]; then
       echo "Task $task_name is already completed. Skipping."
       continue
     fi
     
     echo "========================================="
     echo "Starting Task: $task_name"
     echo "========================================="
     
     node /Users/garymei/Downloads/projects/gnhf-test/dist/cli.mjs --worktree "${task_name}: Run the task specified in $task_file following the /research-cycle workflow."
     
     echo "Waiting 5 seconds for daemon release..."
     sleep 5
   done
   ```
