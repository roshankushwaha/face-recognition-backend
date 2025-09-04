
from fastapi import APIRouter, HTTPException;
from pydantic import BaseModel;
from app.utils.face_utils import detect_and_crop_face;
import base64;
from PIL import Image
import numpy as np
from io import BytesIO
from app.utils.embedding_utils import get_face_embedding, cosine_similarity
from app.db.database import insert_user, get_user_by_email, get_user_by_email_send
from app.utils.hashing import verify_password
import cv2

# signup Login
class SignupRequest(BaseModel):
    name:str
    email: str
    contact: str
    password: str
    image : str

router  = APIRouter()

@router.post("/signup")
async def signup(payload:SignupRequest):
    name = payload.name
    email = payload.email
    contact = payload.contact
    password = payload.password
    image_base64 = payload.image

    #checking if user alreay exists or not
    existing_user = get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # decoding image
    try:
        image_data = base64.b64decode(image_base64.split(",")[-1])
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Image 😭")

    
    # detecting face and cropping 
    cropped_image = detect_and_crop_face(image_np)
    if cropped_image is None:
        raise HTTPException(status_code=422, detail="Face not Detected, Please upload a clear image");

    
    # Get face embedding (128-d vector)
    try:
        embedding = get_face_embedding(cropped_image)
        embedding_list = embedding.tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")
    


    # Insert user into DB
    user_data = insert_user(name, contact, email, password, embedding_list)
    if not user_data:
        raise HTTPException(status_code=500, detail="User registration failed ❌")

    

    return {
        "message": "User successfully signed up 🎉",
        "user": user_data
    }


# Login Logic

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(payload: LoginRequest):
    email = payload.email
    password = payload.password

    # getting user from databaase
    user =get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    

    # verifying password 
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")
    return {
        "message": "Email and password verified. Proceed with face verification.",
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }


class FaceVerifyRequest(BaseModel):
    email: str
    image: str

@router.post("/verify-face")
async def verify_face(payload: FaceVerifyRequest):
    email = payload.email
    image_base64 = payload.image

    # decoding the base64 image 
    try:
        image_data = base64.b64decode(image_base64.split(",")[-1])
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Image 😭")
    
     # detecting face and cropping 
    cropped_image = detect_and_crop_face(image_np)
    if cropped_image is None:
        raise HTTPException(status_code=422, detail="Face not Detected, Please upload a clear image");

    # Get face embedding (128-d vector)
    try:
        input_embedding = get_face_embedding(cropped_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed: {str(e)}")

    # Fetch user from DB
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
     # Convert stored embedding back to numpy array
    stored_embedding = np.array(eval(user["face_embedding"]))  # Stored as string in DB
    # Compare embeddings
    print("Input Embedding:", input_embedding[:5])
    print("Stored Embedding:", stored_embedding[:5])
    print("Input Norm:", np.linalg.norm(input_embedding))
    print("Stored Norm:", np.linalg.norm(stored_embedding))
    embedding = get_face_embedding(cropped_image)
    print("Embedding generated:", embedding[:5])  # ✅ Place it here instead

    
    similarity = cosine_similarity(input_embedding, stored_embedding)
    print("Cosine Similarity Score 🧠:", similarity)
    if similarity > 0.7:  
        return {
            "message": "Face verified ✅", 
            "similarity": similarity, 
            "data": {
                "name":user["name"],
                "email":user["email"],
                "contact":user["contact"],
            }
        }
    else:
        raise HTTPException(status_code=401, detail="Face verification failed ❌")
    


class VerifyTwoFaces(BaseModel):
    image1: str
    image2: str

@router.post("/compare-face")
async def compare_face(payload: VerifyTwoFaces):
    image_base64_1 = payload.image1
    image_base64_2 = payload.image2

    try:
        # Decode base64 → image 1
        image_data1 = base64.b64decode(image_base64_1.split(",")[-1])
        image1 = Image.open(BytesIO(image_data1)).convert("RGB")
        image_np1 = np.array(image1)

        # Decode base64 → image 2
        image_data2 = base64.b64decode(image_base64_2.split(",")[-1])
        image2 = Image.open(BytesIO(image_data2)).convert("RGB")
        image_np2 = np.array(image2)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format 😭 - {str(e)}")

    # Process Face 1
    face1_data = detect_and_crop_face(image_np1)
    if face1_data is None:
        raise HTTPException(status_code=422, detail="Face not detected in Image 1. Please upload a clear image.")

    embedding1_image, face1_bgr = face1_data
    cv2.imwrite("face1.jpg", face1_bgr)

    # Process Face 2
    face2_data = detect_and_crop_face(image_np2)
    if face2_data is None:
        raise HTTPException(status_code=422, detail="Face not detected in Image 2. Please upload a clear image.")

    embedding2_image, face2_bgr = face2_data
    cv2.imwrite("face2.jpg", face2_bgr)

    # Generate Embeddings
    try:
        input_embedding1 = get_face_embedding(embedding1_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed for image 1: {str(e)}")

    try:
        input_embedding2 = get_face_embedding(embedding2_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding generation failed for image 2: {str(e)}")

    # Debug prints
    print("Embedding 1 (first 5 values):", input_embedding1[:5])
    print("Embedding 2 (first 5 values):", input_embedding2[:5])

    # Compare embeddings using cosine similarity
    similarity = cosine_similarity(input_embedding1, input_embedding2)
    print("Cosine Similarity Score 🧠:", similarity)

    # Return response   
    if similarity > 0.7:
        return {
            "message": "Face verified ✅",
            "similarity": float(similarity)
        }
    else:
        raise HTTPException(status_code=401, detail="Face verification failed ❌")