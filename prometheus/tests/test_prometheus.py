from unittest import mock

from django.conf import settings
from django.test import TestCase
from prometheus.signals import (
    membership_request_fail,
    membership_request_success,
    transaction_fail,
    transaction_success,
)


class TestPrometheus(TestCase):
    @mock.patch("prometheus.apps.Counter.inc", autospec=True)
    @mock.patch("prometheus.apps.Counter.labels", autospec=True)
    def test_membership_request_fail(self, mock_prometheus_counter_labels, mock_prometheus_counter_inc):
        """
        Test that the membership request fail counter increments OK
        """
        # GIVEN
        settings.PUSH_PROMETHEUS_METRICS = False  # Disable the attempted push
        # WHEN
        membership_request_fail.send(sender=self)
        # THEN
        mock_prometheus_counter_inc.assert_called_once()
        assert not mock_prometheus_counter_labels.called

    @mock.patch("prometheus.apps.Counter.inc", autospec=True)
    @mock.patch("prometheus.apps.Counter.labels", autospec=True)
    def test_membership_request_success(self, mock_prometheus_counter_labels, mock_prometheus_counter_inc):
        """
        Test that the membership request success counter increments OK
        """
        # GIVEN
        settings.PUSH_PROMETHEUS_METRICS = False  # Disable the attempted push
        # WHEN
        membership_request_success.send(sender=self)
        # THEN
        mock_prometheus_counter_inc.assert_called_once()
        assert not mock_prometheus_counter_labels.called

    @mock.patch("prometheus.apps.Counter.inc", autospec=True)
    @mock.patch("prometheus.apps.Counter.labels", autospec=True)
    def test_transaction_fail(self, mock_prometheus_counter_labels, mock_prometheus_counter_inc):
        """
        Test that the transaction fail counter increments OK
        """
        # GIVEN
        settings.PUSH_PROMETHEUS_METRICS = False  # Disable the attempted push
        # WHEN
        transaction_fail.send(sender=self)
        # THEN
        mock_prometheus_counter_inc.assert_called_once()
        assert not mock_prometheus_counter_labels.called

    @mock.patch("prometheus.apps.Counter.inc", autospec=True)
    @mock.patch("prometheus.apps.Counter.labels", autospec=True)
    def test_transaction_success(self, mock_prometheus_counter_labels, mock_prometheus_counter_inc):
        """
        Test that the transaction success counter increments OK
        """
        # GIVEN
        settings.PUSH_PROMETHEUS_METRICS = False  # Disable the attempted push
        # WHEN
        transaction_success.send(sender=self)
        # THEN
        mock_prometheus_counter_inc.assert_called_once()
        assert not mock_prometheus_counter_labels.called
