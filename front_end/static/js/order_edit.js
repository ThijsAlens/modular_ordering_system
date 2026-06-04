/**
 * Runs automatically when the page loads to fetch and display the order data.
 */
async function loadPage() {
    const orderId = document.getElementById("hidden-order-id").value;
    const tableRefEl = document.getElementById("display-table-reference");
    const ticketsBodyEl = document.getElementById("tickets-table-body");

    try {
        const order = await getOrderById(orderId);
        tableRefEl.innerText = order.table_reference;
        renderTickets(order, ticketsBodyEl);
    } catch (error) {
        console.error("Failed to load order:", error);
        ticketsBodyEl.innerHTML = `<tr><td colspan="4" style="color:red;">Error: ${error.message}</td></tr>`;
        tableRefEl.innerText = "Error loading table";
    }
}

/**
 * Generates the HTML table rows for the tickets and injects them.
 * @param {Object} order - The order object containing tickets.
 * @param {HTMLElement} tbodyEl - The table body element.
 */
function renderTickets(order, tbodyEl) {
    const tickets = order.tickets;
    tbodyEl.innerHTML = ""; // Clear the "Loading..." text

    // 1. ALWAYS render the "+ New Ticket" button as the top row
    const actionRow = document.createElement("tr");
    actionRow.innerHTML = `
        <td colspan="4" style="padding: 0;">
            <button id="new-ticket_button" onclick="newTicket_button()" class="primary">
                + New Ticket
            </button>
        </td>
    `;
    tbodyEl.appendChild(actionRow);

    // 2. Handle the empty state if there are no tickets
    if (!tickets || tickets.length === 0) {
        const emptyRow = document.createElement("tr");
        emptyRow.innerHTML = `
            <td colspan="4" style="text-align: center; color: gray;">
                <em>No tickets yet.</em>
            </td>`;
        tbodyEl.appendChild(emptyRow);
        return;
    }

    // 3. Sort tickets newest first (Descending order by timestamp)
    tickets.sort((a, b) => {
        const timeA = a.time_at_creation ? new Date(a.time_at_creation).getTime() : 0;
        const timeB = b.time_at_creation ? new Date(b.time_at_creation).getTime() : 0;
        return timeB - timeA;
    });

    // 4. Loop through the sorted tickets and create a row for each
    tickets.forEach(ticket => {
        const row = document.createElement("tr");
        
        const timeString = new Date(ticket.time_at_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        row.innerHTML = `
            <td>${timeString}</td>
            <td>${ticket.last_editor}</td>
            <td>${ticket.destination}</td>
            <td>
                <a href="/ticket_edit?order_id=${order.order_id}&ticket_id=${ticket.ticket_id}&destination=${ticket.destination}" class="secondary">View</a>
            </td>
        `;
        
        tbodyEl.appendChild(row);
    });
}

/**
 * Handles the click event of the button with id "new-ticket_button"
 */
function newTicket_button() {
    const orderId = document.getElementById("hidden-order-id").value;
    window.location.href = `/choose_from_destination?order_id=${orderId}`;
}

window.onload = loadPage;