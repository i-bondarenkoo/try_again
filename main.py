from fastapi import FastAPI
import uvicorn
from router.task import router as task_router
from router.user import router as user_router

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
