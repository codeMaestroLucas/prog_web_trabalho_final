from pydantic import BaseModel, Field, field_validator
import re

class User(BaseModel):
    """Classe de Usuário.
    
    Herda de BaseModel e representa um usuário completo, incluindo a
    configuração para trabalhar com ORM - converte automaticamente dados de
    objetos ORM (Object-Relational Mapping) para modelos Pydantic."""
    # id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)
    
    class Config:
        from_attributes  = True
    
    
    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        """Função usada para validar e tratar o nome passado pelo usuário para
        o campo passado.

        Args:
            name (str): Nome.

        Raises:
            ValueError: Caso algum caractere especial esteja dentro do nome
            passado.

        Returns:
            str: retorna o nome validado e tratado.
        """
        if any(char in name for char in '!@#$%^&*()'):
            raise ValueError("O nome do usuário não pode conter caracteres especiais.")
            
        return name.title().strip()
    
    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        """Função usada para validar o email fornecido pelo usuário.

        Args:
            email (str): Email.

        Raises:
            ValueError: Caso o email não se enquadre na opção de regex estabelecida
            esse erro será levantado.

        Returns:
            str: Retorna o email validado e tratado.
        """
        email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        
        """
        - Começam (^) com um ou mais caracteres alfanuméricos (letras maiúsculas
        ou minúsculas e dígitos), incluindo sublinhados, pontos, sinais de mais
        ou hífens.
        
        - Seguem (+) com um caractere @.
        
        - Continuam (+) com um ou mais caracteres alfanuméricos ou hífens, que
        representam o domínio.
        
        - Têm um ponto literal.
        OBS: A "\" somente para o compilador entender que é um ponto literal.
        
        - Terminam ($) com um ou mais caracteres alfanuméricos, pontos ou hífens,
        que representam a parte do domínio de topo (como .com, .org, etc.).
        """
        
        if not email_regex.match(email):
            raise ValueError('Endereço de email inválido.')
        
        return email.strip()
    
    @field_validator('password')
    def validate_password(cls, password: str):
        """Função usada para validar a senha fornecida pelo usuário.

        Args:
            password (str): Senha fornecida pelo usuário.

        Raises:
        
            1. ValueError: Caso a senha seja menor que 8 caracteres;
            
            2. ValueError: Caso a senha não tenha um caractere maiúsculo;

            3. ValueError: Caso a senha não tenha um caractere minúculo;
            
            4. ValueError: Caso a senha não tenha um número;

            5. ValueError: Caso a senha não tenha um caractere especial.

        Returns:
            str: Retorna a senha validada.
        """
        if len(password) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')

        if not re.search(r"[A-Z]", password):
            raise ValueError('Senha deve ter pelo menos uma letra maiúscula')

        if not re.search(r"[a-z]", password):
            raise ValueError('Senha deve ter pelo menos uma letra minúscula')

        if not re.search(r"[0-9]", password):
            raise ValueError('Senha deve ter pelo menos um número')

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError('Senha deve ter pelo menos um caractere especial')

        return password