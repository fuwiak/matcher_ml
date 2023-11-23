from fastapi import FastAPI
import pandas as pd
from name_matching.name_matcher import NameMatcher
from routes import router as name_matching_router


app = FastAPI()
# Include the router from routes.py
app.include_router(name_matching_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

