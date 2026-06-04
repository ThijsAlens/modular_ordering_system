// This file contains the JS code for everything to do with handeling orders with the backend
const BACKEND_URL = "http://192.168.0.143:8000";

/**
 * Fetches a single order by its ID.
 * @param {string|number} orderId 
 * @returns {Promise<Object>} The order dictionary.
 */
async function getOrderById(orderId) {
    const response = await fetch(`${BACKEND_URL}/get_order_by_id?order_id=${orderId}`);
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Order ID not found.");
    }
    
    return await response.json();
}

/**
 * Fetches all active orders for a specific table.
 * @param {string} tableRef The table reference to search for.
 * @returns {Promise<Array>} A list of order dictionaries.
 */
async function getOrdersByTableReference(tableRef) {
    const response = await fetch(`${BACKEND_URL}/get_orders_by_table_reference?table_reference=${tableRef}`);
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "No orders found for this table.");
    }
    
    return await response.json();
}

/**
 * Creates a new order for a given table reference.
 * @param {string} tableRef The table reference for the new order.
 * @returns {Promise<Object>} The newly created order dictionary.
 */
async function createNewOrder(tableRef) {
    const response = await fetch(`${BACKEND_URL}/create_new_order?table_reference=${tableRef}`, {
        method: "POST",
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create a new order.");
    }
    
    return await response.json();
 }


