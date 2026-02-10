# autonomy/autonomy_loop.py

import asyncio
from autonomy.async_task_runner import run_task_async

# ye hi main loop hai
async def run_all(context: str):
    tasks = [
        "Identify key repetitive tasks",
        "Analyze tasks for automation potential",
        "Design automation workflows",
        "Estimate productivity gains"
    ]

    for task in tasks:
        print(f"\n📌 TASK: {task}")
        result = await run_task_async(task)
        print("✅ RESULT:", result)


# API yahin se call karegi
async def autonomous_run(context: str):
    await run_all(context)
