from datetime import datetime, timezone
from typing import Optional
from app.database.mongodb_database import get_database
from app.schemas.auth_schema import UserCreate
from app.utils.password_utils import hash_password, verify_password

class UserService:
    def __init__(self):
        self.db = get_database()
        self.user_collection = self.db['users']
    
    async def create_user(self, user: UserCreate) -> dict:
        """
        Crea un nuevo usuario en la base de datos
        """
        user_dict = user.model_dump()
        
        # Encriptar la contraseña
        user_dict["password"] = hash_password(user_dict["password"])
        user_dict["created_at"] = datetime.now(timezone.utc)
        
        result = await self.user_collection.insert_one(user_dict)
        created_user = await self.user_collection.find_one({"_id": result.inserted_id})
        created_user["id"] = str(created_user.pop("_id"))
        
        return created_user
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """
        Busca un usuario por su correo electrónico
        """
        user = await self.user_collection.find_one({"email": email})
        if user:
            user["id"] = str(user.pop("_id"))
            return user
        return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """
        Autentica un usuario verificando email y contraseña
        """
        user = await self.user_collection.find_one({"email": email})
        if not user:
            return None
        
        # Verificar la contraseña
        if not verify_password(password, user["password"]):
            return None
            
        # Si la autenticación es exitosa, preparar datos del usuario
        user["id"] = str(user.pop("_id"))
        # No devuelvas la contraseña en la respuesta
        user_data = {k: v for k, v in user.items() if k != "password"}
        return user_data