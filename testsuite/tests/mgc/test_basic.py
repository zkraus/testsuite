"""
This module contains the very basic tests and their dependencies for MGC

Prerequisites:
* the hub cluster is also a spoke cluster so that everything happens on the only cluster
* multi-cluster-gateways ns is created and set as openshift["project"]
* managedclustersetbinding is created in openshift["project"]
* placement named "local-cluster" is created in openshift["project"] and bound to clusterset
* gateway class "kuadrant-multi-cluster-gateway-instance-per-cluster" is created
* openshift2["project"] is set

Notes:
* dnspolicies are created and bound to gateways automatically by mgc operator
* dnspolicies leak at this moment
"""
from time import sleep

import pytest

pytestmark = [pytest.mark.mgc]


def test_gateway_readiness(gateway):
    """Tests whether the Gateway was successfully placed by having its IP address assigned"""
    assert gateway.is_ready()


def test_smoke(route):
    """
    Tests whether the backend, exposed using the HTTPRoute and Gateway, was exposed correctly,
    having a tls secured endpoint with a hostname managed by MGC
    """
    backend_client = route.client(verify=False)  # self-signed certificate; TBD

    sleep(30)  # wait for DNS record to propagate correctly; TBD

    response = backend_client.get("get")
    assert response.status_code == 200
