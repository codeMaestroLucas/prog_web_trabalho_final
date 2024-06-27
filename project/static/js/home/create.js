document.addEventListener('DOMContentLoaded', function() {
    const createProductButton = document.querySelector('.create-product');
    const createOrderButton = document.querySelector('.create-order');
    const productContainer = document.querySelector('.container.create_products');
    const orderContainer = document.querySelector('.container.create_orders');

    if (createProductButton && productContainer) {
        createProductButton.addEventListener('click', function() {
            productContainer.classList.remove('not-visible');
            productContainer.classList.add('visible');
        });
    }

    if (createOrderButton && orderContainer) {
        createOrderButton.addEventListener('click', function() {
            orderContainer.classList.remove('not-visible');
            orderContainer.classList.add('visible');
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
});