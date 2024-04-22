import asyncio
import aioping


class PingScheduler:
    def __init__(self):
        self.ping_tasks = {}

    async def ping_host(self, host, interval, task_id):
        try:
            print('ping outside loop')

            while True:
                # Assume ping() is your async ping function
                print('ping in loop')
                response_time = await aioping.ping(host)
                print(f"Ping to {host}: {response_time} ms")
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print(f"Task {task_id} cancelled")
        except Exception as e:
            print(e.with_traceback(None))
            print(f"Error pinging {host}: {str(e)}")
        finally:
            print(f"Task {task_id} finished or cancelled")

    async def add_ping_task(self, host, interval, task_id):
        if task_id in self.ping_tasks:
            print(f"Task {task_id} is already running.")
            return
        task = asyncio.create_task(self.ping_host(host, interval, task_id))

        self.ping_tasks[task_id] = task
        print(f"Task {task_id} added.")
        # await task

    def remove_ping_task(self, task_id):
        if task_id in self.ping_tasks:
            task = self.ping_tasks[task_id]
            task.cancel()
            print(f"Task {task_id} cancelled.")
            # Optionally wait for the task to be cancelled
            # You may handle this with an additional async method
            del self.ping_tasks[task_id]
        else:
            print(f"Task {task_id} not found.")

    async def manage_tasks(self):
        while True:
            await asyncio.sleep(1)  # Keep the loop alive

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.manage_tasks())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
