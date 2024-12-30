// document.addEventListener('DOMContentLoaded', function() {
//     const buttons = document.querySelectorAll('.heart-button');

//     buttons.forEach(button => {
//         const productId = button.getAttribute('data-product-id');

//         // Check local storage for the product's wishlist state
//         if (localStorage.getItem(`wishlist_product_${productId}`) === 'true') {
//             button.classList.add('active');
//         }

//         button.addEventListener('click', function() {
//             button.classList.toggle('active');
            
//             if (button.classList.contains('active')) {
//                 // Add product to wishlist in localStorage
//                 localStorage.setItem(`wishlist_product_${productId}`, 'true');
//             } else {
//                 // Remove product from wishlist in localStorage
//                 localStorage.removeItem(`wishlist_product_${productId}`);
//             }
//         });
//     });
// });
