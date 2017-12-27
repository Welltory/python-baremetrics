# -*- coding: utf-8 -*-
import logging

try:
    from urllib.parse import urljoin
except Exception:
    from urlparse import urljoin

import requests

from .exceptions import BaremetricsAPIException, APICallNotImplemented

logger = logging.getLogger('baremetrics')


class BaremetricsClient(object):
    def __init__(self, token, api_version='v1', sandbox=False):
        self.TOKEN = token
        self.API_VERSION = api_version

        if sandbox:
            self.DEBUG = True
            self.BASE_URL = 'https://api-sandbox.baremetrics.com'
        else:
            self.DEBUG = False
            self.BASE_URL = 'https://api.baremetrics.com'

    def __get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.TOKEN),
            'Accept': 'application/json'
        }

    def __get_url(self, url):
        full_url = '/'.join([self.BASE_URL, self.API_VERSION, url])
        return full_url

    def __get(self, url, **params):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        if self.DEBUG:
            logger.info('Sending GET {} to {}'.format(params, full_url))

        r = requests.get(full_url, headers=headers, params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

    def __post(self, url, data):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        if self.DEBUG:
            logger.info('Sending POST {} to {}'.format(data, full_url))

        r = requests.post(full_url, headers=headers, data=data)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

    def __put(self, url, data):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        if self.DEBUG:
            logger.info('Sending PUT {} to {}'.format(data, full_url))

        r = requests.put(full_url, headers=headers, data=data)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

    def __delete(self, url):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        if self.DEBUG:
            logger.info('Sending DELETE to {}'.format(full_url))

        r = requests.delete(full_url, headers=headers)
        if r.status_code in (requests.codes.ok, requests.codes.accepted,):
            return r.json()
        raise BaremetricsAPIException(r)

    # account

    def get_account(self):
        """
        :return:
        {
          "account": {
            "id": 'account_id',
            "default_currency": {
              "id": "usd",
              "alternate_symbols": [
                "US$"
              ],
              "decimal_mark": ".",
              "disambiguate_symbol": "US$",
              "html_entity": "$",
              "iso_code": "USD",
              "iso_numeric": "840",
              "name": "United States Dollar",
              "priority": 1,
              "smallest_denomination": 1,
              "subunit": "Cent",
              "subunit_to_unit": 100,
              "symbol": "$",
              "symbol_first": true,
              "thousands_separator": ","
            },
            "company": "Example Company",
            "created_at": 123456789
          }
        }
        """
        return self.__get('account')

    # sources

    def list_sources(self):
        """
        :return:
        {
          "sources": [
            {
              "id": "source_id",
              "provider": "stripe",
              "provider_id": "<stripe_account_id>"
            },
            {
              "id": "source_id",
              "provider": "baremetrics",
              "provider_id": null
            }
          ]
        }
        """
        return self.__get('sources')

    # plans

    def list_plans(self, source_id):
        """
        :param source_id: Source ID
        :return:
        {
          "plans": [
            {
              "oid": "plan_1",
              "source_id": "123",
              "source": "baremetrics",
              "name": "Plan 1",
              "interval": "year",
              "interval_count": 1,
              "trial_duration": null,
              "trial_duration_unit": null,
              "created": null,
              "active": true,
              "setup_fees": 0,
              "amounts": [
                {
                  "currency": "USD",
                  "symbol": "$",
                  "symbol_right": false,
                  "amount": 450000
                }
              ]
            },
            {
              "oid": "plan_2",
              "source_id": "123",
              "source": "baremetrics",
              "name": "Plan 2",
              "interval": "year",
              "interval_count": 1,
              "trial_duration": null,
              "trial_duration_unit": null,
              "created": null,
              "active": true,
              "setup_fees": 0,
              "amounts": [
                {
                  "currency": "USD",
                  "symbol": "$",
                  "symbol_right": false,
                  "amount": 450000
                }
              ]
            }
          ]
        }

        """
        return self.__get('{}/plans'.format(source_id))

    def show_plan(self, source_id, plan_id):
        """
        :param source_id: Source ID
        :param plan_id: Plan ID
        :return:
        {
          "plan": {
            "oid": "plan_2",
            "source_id": "123",
            "source": "baremetrics",
            "name": "Plan 2",
            "interval": "year",
            "interval_count": 1,
            "trial_duration": null,
            "trial_duration_unit": null,
            "created": null,
            "active": true,
            "setup_fees": 0,
            "amounts": [
              {
                "currency": "USD",
                "symbol": "$",
                "symbol_right": false,
                "amount": 450000
              }
            ]
          }
        }
        """
        return self.__get('{}/plans/{}'.format(source_id, plan_id))

    def update_plan(self, source_id, oid, name):
        return self.__put('{}/plans/{}'.format(source_id, oid), data={'name': name})

    def create_plan(self, source_id, oid, name, currency, amount, interval, interval_count):
        return self.__post('{}/plans'.format(source_id), data={
            'oid': oid,
            'name': name,
            'currency': currency,
            'amount': amount,
            'interval': interval,
            'interval_count': interval_count
        })

    def delete_plan(self, source_id, oid):
        return self.__delete('{}/plans/{}'.format(source_id, oid))

    # customers

    def list_customers(self, source_id):
        return self.__get('{}/customers'.format(source_id))

    def show_customer(self, source_id, oid):
        return self.__get('{}/customers/{}'.format(source_id, oid))

    def show_customer_events(self, source_id, oid):
        return self.__get('{}/customers/{}/events'.format(source_id, oid))

    def update_customer(self, source_id, customer_oid, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        return self.__put('{}/customers/{}'.format(source_id, customer_oid), data)

    def create_customer(self, source_id, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        return self.__post('{}/customers'.format(source_id), data)

    def delete_customer(self, source_id, oid):
        return self.__delete('{}/customers/{}'.format(source_id, oid))

    # subscriptions

    def list_subscriptions(self, source_id):
        return self.__get('{}/subscriptions'.format(source_id))

    def show_subscription(self, source_id, oid):
        return self.__get('{}/subscriptions/{}'.format(source_id, oid))

    def update_subscription(self, source_id, subscription_oid, plan_oid, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        data.update({
            'plan_id': plan_oid
        })
        return self.__put(
            '{}/subscriptions/{}'.format(source_id, subscription_oid),
            data)

    def cancel_subscription(self, source_id, subscription_oid, canceled_at):
        return self.__put(
            '{}/subscriptions/{}'.format(source_id, subscription_oid),
            data={'canceled_at': canceled_at})

    def create_subscription(self, source_id, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        return self.__post('{}/subscriptions'.format(source_id), data)

    def delete_subscription(self, source_id, subscription_oid):
        return self.__delete('{}/subscriptions/{}'.format(source_id, subscription_oid))

    # annotations

    def list_annotations(self):
        return self.__get('annotations')

    def show_annotation(self, annotation_id):
        return self.__get('annotations/{}'.format(annotation_id))

    def create_annotation(self, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        return self.__post('annotations', data)

    def delete_annotation(self, annotation_id):
        return self.__delete('annotations/{}'.format(annotation_id))

    # goals

    def list_goals(self):
        raise APICallNotImplemented

    def show_goal(self):
        raise APICallNotImplemented

    def create_goal(self):
        raise APICallNotImplemented

    def delete_goal(self):
        raise APICallNotImplemented

    # users

    def list_users(self):
        return self.__get('users')

    def show_user(self, oid):
        return self.__get_url('users/{}'.format(oid))

    # charges

    def list_charges(self, source_id):
        return self.__get('{}/charges'.format(source_id))

    def show_charge(self, source_id, oid):
        return self.__get('{}/charges/{}'.format(source_id, oid))

    def create_charge(self, source_id, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        return self.__post('{}/charges'.format(source_id), data)

    # events

    def list_events(self, source_id):
        return self.__get('{}/events'.format(source_id))

    def show_event(self, source_id, oid):
        return self.__get('{}/events/{}'.format(source_id, oid))

    # metrics

    def show_summary(self):
        raise APICallNotImplemented

    def show_metric(self):
        raise APICallNotImplemented

    def show_customers(self):
        raise APICallNotImplemented

    def show_plan_breakout(self):
        raise APICallNotImplemented
