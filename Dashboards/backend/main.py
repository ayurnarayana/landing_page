from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import jwt
from passlib.context import CryptContext

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY exists:", SUPABASE_KEY is not None)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Ayur Narayana Backend API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ==================== Pydantic Models ====================

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    role: str  # 'admin' or 'therapist'
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: str
    role: str
    created_at: str

class RequestCreate(BaseModel):
    patient_name: str
    phone: str
    email: Optional[str] = None
    location: str
    condition: str
    preferred_time: Optional[str] = None
    notes: Optional[str] = None

class RequestUpdate(BaseModel):
    status: Optional[str] = None
    therapist_id: Optional[str] = None
    notes: Optional[str] = None

class SessionNoteCreate(BaseModel):
    request_id: str
    therapist_id: str
    notes: str

class NotificationCreate(BaseModel):
    user_id: str
    title: str
    message: str

# ==================== Helper Functions ====================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    # Fetch user from database
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    if not response.data:
        raise HTTPException(status_code=401, detail="User not found")
    
    return response.data[0]

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ==================== Authentication Routes ====================

@app.post("/api/auth/register")
async def register(user: UserCreate):
    """Register a new user (admin or therapist)"""
    try:
        # Check if user already exists
        existing = supabase.table("users").select("*").eq("email", user.email).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = hash_password(user.password)
        
        # Insert user
        new_user = {
            "name": user.name,
            "phone": user.phone,
            "email": user.email,
            "role": user.role,
            "password": hashed_password
        }
        
        response = supabase.table("users").insert(new_user).execute()
        
        return {"message": "User registered successfully", "user": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login")
async def login(credentials: UserLogin):
    """Login and get access token"""
    try:
        # Fetch user
        response = supabase.table("users").select("*").eq("email", credentials.email).execute()
        
        if not response.data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = response.data[0]
        
        # Verify password
        if not verify_password(credentials.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token = create_access_token({"user_id": user["id"], "role": user["role"]})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "phone": current_user["phone"],
        "role": current_user["role"]
    }

# ==================== Patient Requests Routes ====================

@app.post("/api/requests")
async def create_request(request: RequestCreate):
    """Create a new patient request (public endpoint)"""
    try:
        new_request = {
            "patient_name": request.patient_name,
            "phone": request.phone,
            "email": request.email,
            "location": request.location,
            "condition": request.condition,
            "preferred_time": request.preferred_time,
            "notes": request.notes,
            "status": "pending"
        }
        
        response = supabase.table("requests").insert(new_request).execute()
        
        return {"message": "Request submitted successfully", "request": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/requests")
async def get_all_requests(
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all requests (filtered by status if provided)"""
    try:
        query = supabase.table("requests").select("*")
        
        # If therapist, only show their assigned requests
        if current_user["role"] == "therapist":
            query = query.eq("therapist_id", current_user["id"])
        
        # Filter by status if provided
        if status:
            query = query.eq("status", status)
        
        query = query.order("created_at", desc=True)
        response = query.execute()
        
        return {"requests": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/requests/{request_id}")
async def get_request(request_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific request"""
    try:
        response = supabase.table("requests").select("*").eq("id", request_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Request not found")
        
        request_data = response.data[0]
        
        # If therapist, check if it's their request
        if current_user["role"] == "therapist" and request_data["therapist_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return {"request": request_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/requests/{request_id}")
async def update_request(
    request_id: str,
    update: RequestUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a request (assign therapist, update status, add notes)"""
    try:
        # Fetch the request
        response = supabase.table("requests").select("*").eq("id", request_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Request not found")
        
        request_data = response.data[0]
        
        # Prepare update data
        update_data = {}
        
        if update.status:
            update_data["status"] = update.status
        
        if update.notes:
            update_data["notes"] = update.notes
        
        # Only admin can assign therapist
        if update.therapist_id:
            if current_user["role"] != "admin":
                raise HTTPException(status_code=403, detail="Only admin can assign therapists")
            update_data["therapist_id"] = update.therapist_id
            update_data["status"] = "assigned"
        
        # Update the request
        updated = supabase.table("requests").update(update_data).eq("id", request_id).execute()
        
        # If therapist was assigned, create notification
        if update.therapist_id:
            notification = {
                "user_id": update.therapist_id,
                "title": "New Patient Assigned",
                "message": f"You have been assigned to patient: {request_data['patient_name']}",
                "is_read": False
            }
            supabase.table("notifications").insert(notification).execute()
        
        return {"message": "Request updated successfully", "request": updated.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Session Notes Routes ====================

@app.post("/api/session-notes")
async def create_session_note(
    note: SessionNoteCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a session note"""
    try:
        # Verify the request belongs to the therapist
        if current_user["role"] == "therapist":
            request_response = supabase.table("requests").select("*").eq("id", note.request_id).execute()
            if not request_response.data or request_response.data[0]["therapist_id"] != current_user["id"]:
                raise HTTPException(status_code=403, detail="Access denied")
        
        new_note = {
            "request_id": note.request_id,
            "therapist_id": note.therapist_id,
            "notes": note.notes
        }
        
        response = supabase.table("session_notes").insert(new_note).execute()
        
        return {"message": "Session note created successfully", "note": response.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session-notes/{request_id}")
async def get_session_notes(request_id: str, current_user: dict = Depends(get_current_user)):
    """Get all session notes for a request"""
    try:
        # Verify access
        request_response = supabase.table("requests").select("*").eq("id", request_id).execute()
        if not request_response.data:
            raise HTTPException(status_code=404, detail="Request not found")
        
        if current_user["role"] == "therapist" and request_response.data[0]["therapist_id"] != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        response = supabase.table("session_notes").select("*").eq("request_id", request_id).order("created_at", desc=True).execute()
        
        return {"notes": response.data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Therapist Routes ====================

@app.get("/api/therapists")
async def get_all_therapists(current_user: dict = Depends(get_admin_user)):
    """Get all therapists (admin only)"""
    try:
        response = supabase.table("users").select("id, name, phone, email, created_at").eq("role", "therapist").execute()
        return {"therapists": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Notifications Routes ====================

@app.get("/api/notifications")
async def get_notifications(current_user: dict = Depends(get_current_user)):
    """Get all notifications for current user"""
    try:
        response = supabase.table("notifications").select("*").eq("user_id", current_user["id"]).order("created_at", desc=True).execute()
        return {"notifications": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, current_user: dict = Depends(get_current_user)):
    """Mark a notification as read"""
    try:
        response = supabase.table("notifications").update({"is_read": True}).eq("id", notification_id).eq("user_id", current_user["id"]).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {"message": "Notification marked as read"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications/unread/count")
async def get_unread_count(current_user: dict = Depends(get_current_user)):
    """Get count of unread notifications"""
    try:
        response = supabase.table("notifications").select("*", count="exact").eq("user_id", current_user["id"]).eq("is_read", False).execute()
        return {"count": response.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Dashboard Statistics ====================

@app.get("/api/stats")
async def get_statistics(current_user: dict = Depends(get_current_user)):
    """Get dashboard statistics"""
    try:
        stats = {}
        
        if current_user["role"] == "admin":
            # Total requests
            total = supabase.table("requests").select("*", count="exact").execute()
            stats["total_requests"] = total.count
            
            # Pending requests
            pending = supabase.table("requests").select("*", count="exact").eq("status", "pending").execute()
            stats["pending_requests"] = pending.count
            
            # Assigned requests
            assigned = supabase.table("requests").select("*", count="exact").eq("status", "assigned").execute()
            stats["assigned_requests"] = assigned.count
            
            # In progress
            in_progress = supabase.table("requests").select("*", count="exact").eq("status", "in_progress").execute()
            stats["in_progress_requests"] = in_progress.count
            
            # Completed
            completed = supabase.table("requests").select("*", count="exact").eq("status", "completed").execute()
            stats["completed_requests"] = completed.count
            
            # Total therapists
            therapists = supabase.table("users").select("*", count="exact").eq("role", "therapist").execute()
            stats["total_therapists"] = therapists.count
            
        else:  # Therapist
            # My assigned requests
            assigned = supabase.table("requests").select("*", count="exact").eq("therapist_id", current_user["id"]).eq("status", "assigned").execute()
            stats["assigned_to_me"] = assigned.count
            
            # In progress
            in_progress = supabase.table("requests").select("*", count="exact").eq("therapist_id", current_user["id"]).eq("status", "in_progress").execute()
            stats["in_progress"] = in_progress.count
            
            # Completed by me
            completed = supabase.table("requests").select("*", count="exact").eq("therapist_id", current_user["id"]).eq("status", "completed").execute()
            stats["completed_by_me"] = completed.count
        
        return {"stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== Health Check ====================

@app.get("/")
async def root():
    return {"message": "Ayur Narayana Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)