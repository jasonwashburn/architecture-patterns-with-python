from datetime import UTC, datetime

from model import Batch, OrderLine


def make_batch_and_line(
    sku: str,
    batch_qty: int,
    line_qty: int,
) -> tuple[Batch, OrderLine]:
    return (
        Batch("batch-001", sku, batch_qty, eta=datetime.now(tz=UTC)),
        OrderLine("order-123", sku, line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity() -> None:
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=datetime.now(tz=UTC))
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required() -> None:
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_less_than_required() -> None:
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_allocation_is_idempotent() -> None:
    batch, line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_equal_to_required() -> None:
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match() -> None:
    batch = Batch("batch-001", "ELEGANT-LAMP", 2, datetime.now(tz=UTC))
    line = OrderLine("order-123", "UNCOMFORTABLE-CHAIR", 2)

    assert batch.can_allocate(line) is False


def test_can_deallocate_allocated_lines() -> None:
    batch, line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    batch.allocate(line)
    assert batch.available_quantity == 18
    batch.deallocate(line)
    assert batch.available_quantity == 20


def test_can_only_deallocate_allocated_lines() -> None:
    batch, line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    batch.deallocate(line)
    assert batch.available_quantity == 20
