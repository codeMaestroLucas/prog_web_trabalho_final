from pydantic import BaseModel, field_validator

class Order(BaseModel):
    """Classe de Pedido.
    
    Herda de BaseModel e representa um pedido completo, incluindo a
    configuração para trabalhar com ORM - converte automaticamente dados de
    objetos ORM (Object-Relational Mapping) para modelos Pydantic."""
    # id: int
    user_id: int
    product_id: int
    quantity: int
    # total_value: float
    
    class Config:
        from_attributes  = True

    @field_validator('quantity')
    def validate_quantity(cls, quantity: int) -> int:
        """Função usada para fazer a validação do valor do campo "quantity"
        fornecido pelo usuário.

        Args:
            quantity (int): Quantidade.

        Raises:
            
            1. ValueError: Quando o valor fornecido não for numérico;
            
            2. ValueError: Quando o valor fornecido for menor ou igual a zero.

        Returns:
            int: Retorna o valor de quantidade validado.
        """
        if not isinstance(quantity, int):
            raise ValueError("A quantidade deve ser um valor numérico inteiro.")
        
        if quantity <= 0:
            raise ValueError("A quantidade do produto não pode ser menor ou igual a 0.")
        
        return quantity