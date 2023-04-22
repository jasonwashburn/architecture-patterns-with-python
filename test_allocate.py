from datetime import UTC, date, datetime, timedelta

import pytest
from model import Batch, OrderLine, OutOfStockError, allocate


@pytest.fixture()
def today() -> date:
    return datetime.now(tz=UTC).date()


@pytest.fixture()
def tomorrow() -> date:
    return datetime.now(tz=UTC).date() + timedelta(days=1)


@pytest.fixture()
def later() -> date:
    return datetime.now(tz=UTC).date() + timedelta(days=2)


def test_prefers_current_stock_batches_to_shipments(today) -> None:
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=today)
    line = OrderLine("order-123", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_current_earlier_batches(today, tomorrow, later) -> None:
    earliest = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=today)
    medium = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    latest = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=later)
    line = OrderLine("order-123", "RETRO-CLOCK", 10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref(tomorrow) -> None:
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate(today) -> None:
    batch = Batch("batch1", "SMALL-FORK", 10, eta=today)
    allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])

    with pytest.raises(OutOfStockError, match="SMALL-FORK"):
        allocate(OrderLine("order2", "SMALL-FORK", 10), [batch])
