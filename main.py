from fastapi import FastAPI
import uvicorn
from router.task import router as task_router

app = FastAPI()
app.include_router(task_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
