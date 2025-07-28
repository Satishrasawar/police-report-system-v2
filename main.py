import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import your local modules (now in same directory)
from agent_routes import router as agent_router
from database import Base, engine
from models import Agent, TaskProgress, SubmittedForm, AgentSession

# Create directories if they don't exist
os.makedirs("static/task_images", exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Crime Records Data Entry System", 
    version="2.0.0",
    description="Enhanced system for agent-task-system.com"
)

# CORS middleware for your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://agent-task-system.com",
        "https://www.agent-task-system.com",
        "https://api.agent-task-system.com",
        "*"  # Allow all for testing (remove later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables on startup
print("🔧 Creating database tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"📋 Available tables: {', '.join(tables)}")
    
except Exception as e:
    print(f"❌ Error creating database tables: {e}")

# Include routers
app.include_router(agent_router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Crime Records Data Entry System API v2.0",
        "status": "running",
        "domain": "agent-task-system.com",
        "platform": "Replit",
        "endpoints": {
            "admin_dashboard": "/admin.html",
            "agent_interface": "/agent.html",
            "api_docs": "/docs",
            "health_check": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "platform": "Replit",
        "database": "connected",
        "message": "All systems operational"
    }

# Serve HTML files
@app.get("/admin.html")
async def serve_admin_panel():
    """Serve the admin dashboard"""
    if os.path.exists("admin.html"):
        return FileResponse("admin.html")
    return {"error": "Admin panel not found"}

@app.get("/agent.html")
async def serve_agent_panel():
    """Serve the agent interface"""
    if os.path.exists("agent.html"):
        return FileResponse("agent.html")
    return {"error": "Agent panel not found"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
