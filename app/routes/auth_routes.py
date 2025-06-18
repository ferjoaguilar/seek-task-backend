from fastapi import APIRouter,HTTPException, status, Body
from app.schemas.auth_schema import TokenType, UserCreate, UserLogin
from app.services.auth_services import UserService
from app.utils.auth_utils import generate_jwt

auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED, 
                  responses={
                      201: {
                          "description": "Usuario registrado exitosamente",
                          "content": {
                              "application/json": {
                                  "example": {
                                      "message": "Usuario registrado exitosamente",
                                      "user_id": "1234567890abcdef",
                                      "email": "jgon@gmail.com",
                                      "username": "jgon"
                                    }
                                }
                            }
                        },
                  })
async def register_user(user_data: UserCreate):
    """
    Registra un nuevo usuario en el sistema
    """
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    user = await user_service.create_user(user_data)
    return {
        "message": "Usuario registrado exitosamente",
        "user_id": user["id"],
        "email": user["email"],
        "username": user["username"]
    }

@auth_router.post("/login", status_code=status.HTTP_200_OK, 
                 responses={
                     200: {
                         "description": "Login exitoso",
                         "content": {
                             "application/json": {
                                 "example": {
                                     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                     "token_type": "bearer",
                                     "user_id": "1234567890abcdef",
                                     "username": "jgon"
                                 }
                             }
                         }
                     },
                     401: {
                         "description": "Credenciales inválidas",
                         "content": {
                             "application/json": {
                                 "example": {
                                     "detail": "Credenciales incorrectas"
                                 }
                             }
                         }
                     }
                 })
async def login(login: UserLogin = Body()):
    """
    Autentica a un usuario y genera un token JWT
    """
    user = await user_service.authenticate_user(
        email=login.email, 
        password=login.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Generar token JWT
    import os
    secret_key = os.getenv("JWT_SECRET_ACCESS")
    if not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Secret JWT access key is not set"
        )
    
    # Payload con información del usuario
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "username": user["username"]
    }
    
    # Generar token con expiración de 30 minutos
    token = generate_jwt(payload, secret_key, TokenType.ACCESS, expires=30)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user["id"],
        "username": user["username"]
    }