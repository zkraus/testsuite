"""Conftest for the Authorino metrics tests"""

import yaml

import pytest
from openshift_client import selector

from testsuite.gateway.envoy import Envoy
from testsuite.httpx import KuadrantClient
from testsuite.kubernetes.config_map import ConfigMap
from testsuite.kubernetes.service_monitor import ServiceMonitor, MetricsEndpoint
from testsuite.prometheus import Prometheus


@pytest.fixture(scope="package")
def prometheus(cluster):
    """
    Return an instance of Thanos metrics client
    Skip tests if query route is not properly configured
    """
    openshift_monitoring = cluster.change_project("openshift-monitoring")
    # Check if metrics are enabled
    try:
        with openshift_monitoring.context:
            cm = selector("cm/cluster-monitoring-config").object(cls=ConfigMap)
            assert yaml.safe_load(cm["config.yaml"])["enableUserWorkload"]
    except Exception:  # pylint: disable=broad-exception-caught
        pytest.skip("User workload monitoring is disabled")

    # find thanos-querier route in the openshift-monitoring project
    # this route allows to query metrics

    routes = openshift_monitoring.get_routes_for_service("thanos-querier")
    if len(routes) == 0:
        pytest.skip("Skipping metrics tests as query route is not properly configured")

    url = ("https://" if "tls" in routes[0].model.spec else "http://") + routes[0].model.spec.host
    with KuadrantClient(headers={"Authorization": f"Bearer {cluster.token}"}, base_url=url, verify=False) as client:
        yield Prometheus(client)


@pytest.fixture(scope="module")
def gateway(request, authorino, cluster, blame, label, testconfig) -> Envoy:
    """Deploys Envoy that wires up the Backend behind the reverse-proxy and Authorino instance"""
    gw = Envoy(
        cluster,
        blame("gw"),
        authorino,
        testconfig["service_protection"]["envoy"]["image"],
        labels={"app": label},
    )
    request.addfinalizer(gw.delete)
    gw.commit()
    gw.wait_for_ready()
    return gw


@pytest.fixture(scope="module")
def authorino(authorino, module_label):
    """Label Authorino controller-metrics service for the proper discovery"""
    authorino.metrics_service.label({"app": module_label})
    return authorino


@pytest.fixture(scope="module")
def service_monitor(cluster, prometheus, blame, module_label):  # pylint: disable=unused-argument
    """Create ServiceMonitor object to follow Authorino /metrics and /server-metrics endpoints"""
    endpoints = [MetricsEndpoint("/metrics", "http"), MetricsEndpoint("/server-metrics", "http")]
    return ServiceMonitor.create_instance(cluster, blame("sm"), endpoints, match_labels={"app": module_label})


@pytest.fixture(scope="module", autouse=True)
def commit(commit, prometheus, request, service_monitor):  # pylint: disable=unused-argument
    """Commit service monitor object"""
    request.addfinalizer(service_monitor.delete)
    service_monitor.commit()
    assert prometheus.is_reconciled(service_monitor), "Service Monitor didn't get reconciled in time"