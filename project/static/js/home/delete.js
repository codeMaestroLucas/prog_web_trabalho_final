document.addEventListener('DOMContentLoaded', function() {
    const deleteProductButton = document.querySelectorAll('.delete-product');
    const deleteOrderButton = document.querySelectorAll('.delete-order');
    const productContainer = document.querySelector('.container.delete_products');
    const orderContainer = document.querySelector('.container.delete_orders');

    if (deleteProductButton.length > 0 && productContainer) {
        deleteProductButton.forEach(button => {
            button.addEventListener('click', function() {
                productContainer.classList.remove('not-visible');
                productContainer.classList.add('visible');
            });
        });
    }

    if (deleteOrderButton.length > 0 && orderContainer) {
        deleteOrderButton.forEach(button => {
            button.addEventListener('click', function() {
                orderContainer.classList.remove('not-visible');
                orderContainer.classList.add('visible');
            });
        });
    }

    const closeButtons = document.querySelectorAll('.btn-close');

    if (closeButtons.length > 0) {
        closeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const container = this.closest('.container');
                if (container) {
                    container.classList.remove('visible');
                    container.classList.add('not-visible');
                }
            });
        });
    }

    const updateButtons = document.querySelectorAll('.btn.update');

    if (updateButtons.length > 0) {
        updateButtons.forEach(button => {
            button.addEventListener('click', function() {
                let id = '';

                if (button.classList.contains('update-product')) {
                    id = document.querySelector('.prod_data.id').textContent.trim();
                } else if (button.classList.contains('update-order')) {
                    id = document.querySelector('.order_data.total_value').textContent.trim();
                }
            });
        });
    }
});