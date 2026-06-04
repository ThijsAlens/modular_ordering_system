/**
 * Creates a new, empty ticket for a specific order.
 * @param {int} orderId The ID of the order.
 * @param {Destination} destination The destination for which to fetch the menu.
 * @param {Array} items The list of items to include in the ticket.
 * @param {string} comment An optional comment to include with the ticket.
 * @param {string} creator The name of the ticket creator (e.g., Jos).
 * @returns {Promise<Object>} The newly created ticket dictionary.
 */
async function createNewTicket(orderId, destination, items, comment, lastEditor) {
    const url = `${BACKEND_URL}/create_new_ticket?order_id=${orderId}&destination=${destination}&comment=${comment}&last_editor=${lastEditor}`;
    
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(items) 
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create a new ticket.");
    }
    
    return await response.json();
}

async function updateTicketByIds(orderId, ticketId, newItems, newComment, lastEditor) {
    const url = `${BACKEND_URL}/update_ticket_by_ids?order_id=${orderId}&ticket_id=${ticketId}&new_comment=${newComment}&last_editor=${lastEditor}`;
    
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newItems)
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to update ticket.");
    }

    return await response.json();
}

async function getTicketByIds(orderId, ticketId) {
    const response = await fetch(`${BACKEND_URL}/get_ticket_by_ids?order_id=${orderId}&ticket_id=${ticketId}`, {
        method: "GET",
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to fetch ticket.");
    }

    return await response.json();
}