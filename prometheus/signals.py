import django.dispatch

from prometheus.apps import PrometheusManager

prometheus_manager = PrometheusManager()

membership_request_fail = django.dispatch.Signal()
membership_request_fail.connect(prometheus_manager.membership_request_fail)
membership_request_success = django.dispatch.Signal()
membership_request_success.connect(prometheus_manager.membership_request_success)
transaction_fail = django.dispatch.Signal()
transaction_fail.connect(prometheus_manager.transaction_fail)
transaction_success = django.dispatch.Signal()
transaction_success.connect(prometheus_manager.transaction_success)
