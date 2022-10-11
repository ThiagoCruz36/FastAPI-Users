from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Response, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import uuid
from .database import engine, Base, get_db
from .models import User, Base
from .repositories import UserRepository
from .schemas import UserRequest, UserResponse
from config import Config
from PIL import Image

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def welcome():
    return("Welcome to the FastAPI! This is a API for managing users and images.")

@app.get("/users", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = UserRepository.get_users(db)
    return [UserResponse.from_orm(user) for user in users]


@app.get("/users/{id}", response_model=UserResponse)
def read_user(id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_orm(user)


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserRequest, db: Session = Depends(get_db)):
    verify_user = UserRepository.get_user_by_email(db, email=request.email)
    if verify_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = UserRepository.user_save(db, User(**request.dict()))
    return UserResponse.from_orm(user)


@app.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, request: UserRequest, db: Session = Depends(get_db)):
    if not UserRepository.get_user_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user = UserRepository.user_save(db, User(id=id, **request.dict()))
    return UserResponse.from_orm(user)

@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    if not UserRepository.get_user_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    UserRepository.delete_user(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/user/{id}/images")
async def upload_user_image(id: int, db: Session = Depends(get_db), file: UploadFile = File(...)):

    user = UserRepository.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    path = os.path.join(Config.UPLOADS_FOLDER, "users")

    # If an image already exists for the user, it will be replaced by the new one.
    if user.image_filename != None:
        delete_image = os.path.join(Config.UPLOADS_FOLDER, "users", user.image_filename)
        delete_thumb = os.path.join(Config.UPLOADS_FOLDER, "users", ('thumb_' + user.image_filename))
        os.remove(delete_image, delete_thumb)

    try:
        # Generate a code for the image name
        file.filename = f"{uuid.uuid4()}.jpg"
        filename = file.filename
        contents = await file.read()

        with open(f"{path}/{file.filename}", "wb") as f:
            f.write(contents)

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    # Create a thumb
    thumb_name = 'thumb_' + str(user.id) + '_' + filename + '.png'
    size = (200, 200)
    image = Image.open(os.path.join(Config.UPLOADS_FOLDER, "users", filename))
    image.thumbnail(size, Image.ANTIALIAS)
    background = Image.new('RGBA', size, (255, 255, 255, 0))
    background.paste(image, (int((size[0] - image.size[0]) // 2), int((size[1] - image.size[1]) // 2)))
    background.save(os.path.join(Config.UPLOADS_FOLDER, "users", thumb_name))

    # Add name of image to user
    update_user = UserRepository.user_save(db, User(id=id, image_filename=file.filename, thumb=thumb_name, name=user.name, email=user.email))

    return UserResponse.from_orm(update_user)


@app.get("/users/{id}/images", response_model=UserResponse)
def get_user_image(id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.image_filename == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    image = os.path.join(Config.UPLOADS_FOLDER, "users", user.image_filename)
    
    return FileResponse(image)

@app.get("/users/thumbs", response_model=UserResponse)
def get_user_images_thumbnails(id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.thumb == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumb not found")

    image = os.path.join(Config.UPLOADS_FOLDER, "users", user.thumb)
    
    return FileResponse(image)


@app.delete("/users/{id}/images", response_model=UserResponse)
def delete_user_image(id: int, db: Session = Depends(get_db)):
    user = UserRepository.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.image_filename == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    delete_image = os.path.join(Config.UPLOADS_FOLDER, "users", user.image_filename)
    os.remove(delete_image)

    if user.thumb == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumb not found")

    delete_thumb = os.path.join(Config.UPLOADS_FOLDER, "users", ('thumb_' + user.image_filename))
    os.remove(delete_thumb)

    return ('Deleted image')