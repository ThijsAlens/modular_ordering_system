

from back_end.JSON_filewriter.JSON_filewriter import JSON_Filewriter
from back_end.model.ticket import Ticket
from back_end.enums.destination import Destination


class Filewriter_pending_tickets(JSON_Filewriter):
    """
    A class for managing the "pending_tickets.json" state file.
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def remove_ticket_by_id(self, ticket_id: int) -> bool:
        """
        Removes a ticket from the "pending_tickets.json" file by its ID.

        Args:
            ticket_id (int): The ID of the ticket to be removed.

        Returns:
            bool: True if the ticket was found and removed, False otherwise.
        """
        tickets: list[Ticket] = self.read_everything_from_file(Ticket)
        if tickets is None:
            return False

        updated_tickets = [ticket for ticket in tickets if ticket.get_ticket_id() != ticket_id]

        if len(updated_tickets) == len(tickets):
            return False

        # sort the tickets by their ID to maintain order
        updated_tickets.sort(key=lambda t: t.get_ticket_id())

        self.append_to_file(updated_tickets, truncate=True)
        return True

    def add_ticket(self, ticket: Ticket) -> None:
        """
        Adds a new ticket to the "pending_tickets.json" file.

        Args:
            ticket (Ticket): The ticket to be added.

        Returns:
            None
        """
        curr_tickets: list[Ticket] = self.read_everything_from_file(Ticket)
        curr_tickets.append(ticket)

        # sort the tickets by their ID to maintain order
        curr_tickets.sort(key=lambda t: t.get_ticket_id())
        self.append_to_file(curr_tickets, truncate=True)
        return
    
    def get_ticket_by_id(self, ticket_id: int) -> Ticket | None:
        """
        Retrieves a ticket by its ID.

        Args:
            ticket_id (int): The ID of the ticket to retrieve.

        Returns:
            Ticket | None: The ticket with the specified ID, or None if not found.
        """
        tickets: list[Ticket] = self.read_everything_from_file(Ticket)
        if tickets is None:
            return None

        for ticket in tickets:
            if ticket.get_ticket_id() == ticket_id:
                return ticket

        return None
    
    def get_tickets_by_destination(self, destination: Destination) -> list[Ticket]:
        """
        Retrieves all tickets with the specified destination.

        Args:
            destination (Destination): The destination to filter tickets by.

        Returns:
            list[Ticket]: A list of tickets matching the specified destination, sorted by submission time.
        """
        tickets: list[Ticket] = self.read_everything_from_file(Ticket)
        if tickets is None:
            return []

        filtered_tickets = [ticket for ticket in tickets if ticket.get_destination() == destination]

        # sort the tickets by submission time
        filtered_tickets.sort(key=lambda t: t.get_timestamp())
        return filtered_tickets
    
    def get_tickets_by_order_id(self, order_id: int) -> list[Ticket]:
        """
        Retrieves all tickets associated with the specified order ID.

        Args:
            order_id (int): The order ID to filter tickets by.

        Returns:
            list[Ticket]: A list of tickets matching the specified order ID, sorted by inverse submission time.
        """
        tickets: list[Ticket] = self.read_everything_from_file(Ticket)
        if tickets is None:
            return []

        filtered_tickets = [ticket for ticket in tickets if ticket.get_order_id() == order_id]

        # sort the tickets by submission time
        filtered_tickets.sort(key=lambda t: t.get_timestamp(), reverse=True)
        return filtered_tickets