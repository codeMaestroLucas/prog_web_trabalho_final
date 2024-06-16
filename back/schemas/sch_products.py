from pydantic import BaseModel, Field, field_validator

class Product(BaseModel):
    """Classe de Produto.
    
    Herda de BaseModel e representa um produto completo, incluindo a
    configuração para trabalhar com ORM - converte automaticamente dados de
    objetos ORM (Object-Relational Mapping) para modelos Pydantic."""
    # id: int
    name: str  = Field(..., min_length=1, max_length=100)
    price: float
    in_stock: int
    
    class Config:
        from_attributes  = True
    
    @field_validator('name')
    def validate_name(cls, name: str) -> str:
        """Função usada para validar e tratar o nome passado pelo usuário para
        o campo passado.

        Args:
            name (str): nome.

        Raises:
            ValueError: Essse erro será levantado caso algum caractere especial
            esteja dentro do nome passado.

        Returns:
            str: retorna o nome tratado.
        """
        if any(char in name for char in '!@#$%^&*()'):
            raise ValueError("O nome do produto não pode conter caracteres especiais.")
        
        return name.strip().title()

    
    @field_validator('price')
    def validate_price(cls, price: float) -> float:
        """Função usada para fazer a validação do valor do campo "price"
        fornecido pelo usuário.
        
        Args:
            price (float): preço do produto.

        Raises:
            
            1. ValueError: Quando o valor fornecido não for numérico;
            
            2. ValueError: Quando o valor fornecido for menor ou igual a zero.

        Returns:
            float: Retorna o valor validado e com duas casas decimais.
        """
        if not isinstance(price, (int, float)):
            raise ValueError("O preço do produto deve ser um valor numérico.")
        
        if price <= 0:
            raise ValueError("O preço do produto não pode ser menor ou igual a 0.")
        
        return round(price, 2)
    
    @field_validator('in_stock')
    def validade_in_stock(cls, in_stock: int) -> int:
        """Função usada para fazer a validação do valor do campo "in_stock"
        fornecido pelo usuário.

        Args:
            in_stock (int): produtos em estoque.

        Raises:
            
            1. ValueError: Quando o valor fornecido não for numérico;
            
            2. ValueError: Quando o valor fornecido for menor do que zero.

        Returns:
            int: retorna o valor de produtos em estoque validado.
        """
        if not isinstance(in_stock, int):
            raise ValueError("O nº produtos em estoque deve ser um valor numérico inteiro.")
        
        if in_stock < 0:
            raise ValueError("O nº produtos em estoque do produto não pode ser menor do que 0.")
        
        return in_stock