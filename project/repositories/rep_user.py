from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..schemas.sch_users import User as schUser
from ..models.mod_users import User as modUser
from ..utils.check_if_exists import check_if_exists


class User:
    """Classe usada para realizar as funções solicitadas pelos endpoints.
    """
    def  __init__(self, db: Session) -> None:
        self.db = db
    
    def create_user(self, name: str, email: str, password: str
                    ) -> modUser | dict:
        """Função usada para criar um usuário.

        Args:
            name (str): Nome.
            email (str): Email.
            password (str): Senha.

        Returns:
            modUser | dict: Retorna o usuário criado com sucesso ou um
            dicionário contendo a mensagem de erro caso o email já esteja em uso.
        """
        user  = schUser(name= name, email= email, password= password)
        check_if_exists('user', user, self.db, invert= True)

        try:
            user = modUser(name= name, email= email, password= password)

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()
            return {"message": "Email em uso."}

    def get_user_by_email(self, email: str) -> modUser | None:
        """Função usada para retornar um usuário já registrado no DB com base no
        seu email.

        Args:
            email (str): Email.

        Returns:
            modUser | None: Retorna o usuário, caso exista.
        """
        return self.db.query(modUser).filter(User.email == email).first()


    def get_user_by_id(self, _id: int) -> modUser | None:
        """Função usada para retornar um usuário já registrado no DB com base no
        seu id.

        Args:
            _id (str): ID.

        Returns:
            modUser | None: Retorna o usuário, caso exista.
        """
        return self.db.query(modUser).filter(User.id == _id).first()