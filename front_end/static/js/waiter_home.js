// This file contains the JS code for the 'waiter_home.html' page.

/**
 * Handles the click event of the button with id "find-order_search-button"
 */
async function findOrder_searchButton() {
    const searchType = document.getElementById("find-order_search-type").value;
    const searchValue = document.getElementById("find-order_search-value").value;
    const messageEl = document.getElementById("find-order_error-message");

    messageEl.textContent = ""; // Clear previous error message

    if (!searchValue) {
        messageEl.innerText = "Please enter a value to search.";
        return; 
    }

    try {
        if (searchType === "table-reference") {
            const orders = await getOrdersByTableReference(searchValue);

            if (orders.length === 1) {
                window.location.href = `/order_edit?order_id=${orders[0].order_id}`;
            } else {
                window.location.href = `/order_choose-from-same-table-reference?table_reference=${searchValue}`;
            }
        }
        if (searchType === "order-id") {
            const order = await getOrderById(searchValue);
            window.location.href = `/order_edit?order_id=${order.order_id}`;
        }
    } catch (error) {
        messageEl.innerText = error.message || "Network error: Could not connect to the server.";
    }
}

/**
 * Handles the click event of the button with id "create-order_create-button"
 */
async function createOrder_createButton() {
    const tableReference = document.getElementById("create-order_table-reference").value;
    const messageEl = document.getElementById("create-order_error-message");

    messageEl.textContent = ""; // Clear previous error message

    if (!tableReference) {
        messageEl.innerText = "Please enter a table reference.";
        return; 
    }

    try {
        const new_order = await createNewOrder(tableReference);
        window.location.href = `/order_edit?order_id=${new_order.order_id}`;
        alert(`New order created with ID: ${new_order.order_id}`);
    } catch (error) {
        messageEl.innerText = error.message || "Network error: Could not connect to the server.";
    }
}
