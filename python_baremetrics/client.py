# -*- coding: utf-8 -*-
import logging

try:
    from urllib.parse import urljoin
except Exception:
    from urlparse import urljoin

import requests

from .exceptions import BaremetricsAPIException

logger = logging.getLogger()


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

        r = requests.get(full_url, headers=headers, params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

    def __post(self, url, data):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        r = requests.post(full_url, headers=headers, data=data)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

    def __put(self, url, data):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        r = requests.put(full_url, headers=headers, data=data)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

    def __delete(self, url):
        full_url = self.__get_url(url)
        headers = self.__get_headers()

        r = requests.delete(full_url, headers=headers)
        if r.status_code == requests.codes.ok:
            return r.json()
        raise BaremetricsAPIException(r)

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
