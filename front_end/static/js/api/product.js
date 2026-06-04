
/**
 * 
 * @param {int} productId 
 * @returns {Promise<Object>} The product dictionary for the specified product ID.
 */
async function getProductById(productId) {
    const response = await fetch(`${BACKEND_URL}/get_product_by_id?product_id=${productId}`);
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Failed to fetch product with ID ${productId}.`);
    }
    
    return await response.json();
}