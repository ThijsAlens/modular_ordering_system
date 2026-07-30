async function loadPage() {
    try {
        const tbodyEl_pending_tickets = document.getElementById("pending-tickets_table-body");
        const pendingTickets = await getAllPendingTicketsByDestination("dessert");
        renderPendingTickets(pendingTickets, tbodyEl_pending_tickets);
    } catch (error) {
        tbodyEl_pending_tickets.innerHTML = `<tr><td colspan="4" style="color:red; text-align:center;">Error loading tickets: ${error.message}</td></tr>`;
    }

    try {
        const tbodyEl_completed_tickets = document.getElementById("completed-tickets-table-body");
        const completedTickets = await getAllCompletedTicketsByDestination("dessert");
        renderCompletedTickets(completedTickets, tbodyEl_completed_tickets);
    } catch (error) {
        tbodyEl_completed_tickets.innerHTML = `<tr><td colspan="4" style="color:red; text-align:center;">Error loading completed tickets: ${error.message}</td></tr>`;
    }
}

function renderPendingTickets(tickets, tbodyEl) {
    tbodyEl.innerHTML = ""; // Clear the loading text

    if (!tickets || tickets.length === 0) {
        tbodyEl.innerHTML = `<tr><td colspan="4" style="text-align: center; color: gray;"><em>No pending tickets! Good job :)</em></td></tr>`;
        return;
    }

    tickets.sort((a, b) => {
        const timeA = a.time_at_creation ? new Date(a.time_at_creation).getTime() : 0;
        const timeB = b.time_at_creation ? new Date(b.time_at_creation).getTime() : 0;
        return timeA - timeB; 
    });

    tickets.forEach(ticket => {
        const row = document.createElement("tr");

        let timeString = "Unknown";
        timeString = new Date(ticket.time_at_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        const editorName = ticket.last_editor || "Unknown";

        row.innerHTML = `
            <td>${timeString}</td>
            <td>${editorName}</td>
            <td>
                <a href="/ticket_edit?order_id=${ticket.order_id}&ticket_id=${ticket.ticket_id}&destination=${ticket.destination}" class="secondary">View / Edit</a>
            </td>
            <td>
                <button onclick="completePendingTicket(${ticket.order_id}, ${ticket.ticket_id})" class="primary" style="margin: 0; padding: 0.25rem 1rem;">Complete</button>
            </td>
        `;
        
        tbodyEl.appendChild(row);
    });
}

// Handles the "Complete" button next to a pending ticket
async function completePendingTicket(orderId, ticketId) {
    try {
        await changeTicketStatusByIds(orderId, ticketId, "completed");
        
        loadPage(); // Refresh the ticket list after completion
    } catch (error) {
        alert("Failed to complete ticket: " + error.message);
    }
}

async function renderCompletedTickets(tickets, tbodyEl) {
    tbodyEl.innerHTML = ""; // Clear the loading text

    if (!tickets || tickets.length === 0) {
        tbodyEl.innerHTML = `<tr><td colspan="4" style="text-align: center; color: gray;"><em>No completed tickets yet.</em></td></tr>`;
        return;
    }

    tickets.sort((a, b) => {
        const timeA = a.time_at_creation ? new Date(a.time_at_creation).getTime() : 0;
        const timeB = b.time_at_creation ? new Date(b.time_at_creation).getTime() : 0;
        return timeB - timeA; 
    });

    tickets = tickets.slice(0, 10);

    tickets.forEach(ticket => {
        const row = document.createElement("tr");

        let timeString = "Unknown";
        timeString = new Date(ticket.time_at_creation).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        const editorName = ticket.last_editor || "Unknown";

        row.innerHTML = `
            <td>${timeString}</td>
            <td>${editorName}</td>
            <td>
                <a href="/ticket_edit?order_id=${ticket.order_id}&ticket_id=${ticket.ticket_id}&destination=${ticket.destination}" class="secondary">View / Edit</a>
            </td>
            <td>
                <button onclick="reopenCompletedTicket(${ticket.order_id}, ${ticket.ticket_id})" class="primary" style="margin: 0; padding: 0.25rem 1rem;">Reopen</button>
            </td>
        `;
        
        tbodyEl.appendChild(row);
    });
}

// Handles the "Reopen" button next to a completed ticket
async function reopenCompletedTicket(orderId, ticketId) {
    try {
        await changeTicketStatusByIds(orderId, ticketId, "pending");
        
        loadPage(); // Refresh the ticket list after reopening
    } catch (error) {
        alert("Failed to reopen ticket: " + error.message);
    }
}

window.onload = loadPage;