from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pymongo.errors import ConfigurationError  
import asyncio

from api_router.image_router import router as image_router
from api_router.policy_router import router as policy_router
from api_router.assessment_router import router as assessment_router

from core.init_vision_model import init_vision_model_client
from core.init_storage import init_storage_client
from core.init_DB import init_db_client
from core.init_llm import init_llm_client
from core.init_prompt_optimizer import init_prompt_optimizer

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting lifespan...")
    try:
        init_vision_model_client()
        init_storage_client()
        
        try:
            init_db_client()
        except ConfigurationError as db_err:
            print(f"⚠️ MongoDB configuration error: {db_err}")
            # Optionally: mark DB as unavailable in app state
            app.state.db_available = False
        else:
            app.state.db_available = True

        init_llm_client()
        init_prompt_optimizer()

        print("Initialization completed.")
        yield
    except asyncio.CancelledError:
        print("Lifespan cancelled (probably shutdown signal)")
        raise
    except Exception as e:
        print(f"Unhandled error during lifespan startup: {e}")
        raise
    finally:
        print("Shutting down lifespan...")


app = FastAPI(lifespan=lifespan)

origins = [
    "https://localhost:5241",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image_router, prefix="/api_router", tags=["Image Generation"])
app.include_router(policy_router, prefix="/api_router", tags=["Policy Generation"])
app.include_router(assessment_router, prefix="/api_router", tags=["Assessment"])

@app.get("/")
def root():
    return {"message": "Raily Addon FastAPI server is running!"}
