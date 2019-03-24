import pytest

from copanier.models import Delivery

pytestmark = pytest.mark.asyncio


async def test_empty_home(client):
    resp = await client.get("/")
    assert resp.status == 200


async def test_home_should_list_active_delivery(client, delivery):
    delivery.persist()
    resp = await client.get("/")
    assert resp.status == 200
    assert delivery.producer in resp.body.decode()


async def test_home_should_redirect_to_login_if_not_logged(client):
    client.logout()
    resp = await client.get("/")
    assert resp.status == 302
    assert resp.headers["Location"] == "/sésame?next=/"


async def test_create_delivery(client):
    assert not list(Delivery.all())
    body = {
        "producer": "Andines",
        "where": "Marché de la Briche",
        "date": "2019-02-23",
        "from_time": "18:30:00",
        "to_time": "20:00:00",
        "order_before": "2019-02-12"
    }
    resp = await client.post("/livraison", body=body)
    assert resp.status == 302
    assert len(list(Delivery.all())) == 1
    delivery = list(Delivery.all())[0]
    assert delivery.producer == "Andines"
    assert delivery.from_date.year == 2019
    assert delivery.from_date.hour == 18
    assert delivery.from_date.minute == 30
    assert delivery.to_date.year == 2019
    assert delivery.to_date.hour == 20
    assert delivery.to_date.minute == 0