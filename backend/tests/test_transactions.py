import pytest
from sqlalchemy.orm import Session
from backend.models import Transaction, Ticket, User
from backend.crud.transactions import create_transaction, delete_transaction
from backend.crud.tickets import create_tickets, get_tickets_by_transaction
from backend.schemas import TransactionCreate, TicketCreate, UserCreate
from backend.database import get_db
from datetime import date


@pytest.fixture(scope="function")
def db():
    """
    Fixture dostarczająca instancję sesji bazy danych na potrzeby testów.
    """
    db_generator = get_db()
    db = next(db_generator)  # Pobranie instancji sesji z generatora
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_transaction_data():
    return TransactionCreate(
        id_users=1,
        id_showings=1,
        status="pending",
        date=date.today()
    )


def test_create_and_delete_transaction(sample_transaction_data, db: Session):
    # Dodanie użytkownika do tabeli users

    # Create transaction
    transaction = create_transaction(db, sample_transaction_data)
    assert transaction.id is not None
    assert transaction.status == "pending"

    # Create associated tickets
    ticket1 = TicketCreate(
        id_transaction=transaction.id,
        id_pricelist=1,
        id_seats=1
    )
    ticket2 = TicketCreate(
        id_transaction=transaction.id,
        id_pricelist=1,
        id_seats=2
    )
    create_tickets(db, [ticket1, ticket2])

    # Verify tickets were created
    tickets = db.query(Ticket).filter(Ticket.id_transaction == transaction.id).all()
    assert len(tickets) == 2

    # Delete transaction
    delete_transaction(db, transaction)

    # Verify transaction and tickets were deleted
    deleted_transaction = db.query(Transaction).filter(Transaction.id == transaction.id).first()
    deleted_tickets = db.query(Ticket).filter(Ticket.id_transaction == transaction.id).all()

    assert deleted_transaction is None
    assert len(deleted_tickets) == 0


def test_delete_nonexistent_transaction(db: Session):
    non_existent_transaction = Transaction(id=99999)  # Transaction that doesn't exist
    result = delete_transaction(db, non_existent_transaction)
    assert result is None