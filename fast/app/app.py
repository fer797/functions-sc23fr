from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def background_print_task():
    for i in range(5):
        time.sleep(1)
        print(f"Background task running...{i}")

@app.get("/")
def read_root():
    return {"Hello": "World777777777"}

@app.get("/background")
def run_background_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_print_task)
    return {"message": "Background task started"}

