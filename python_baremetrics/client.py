# -*- coding: utf-8 -*-

try:
    from urllib.parse import urljoin
except Exception:
    from urlparse import urljoin

import requests

from .exceptions import BaremetricsException


class BaremetricsClient(object):
    BASE_URL = 'https://api.baremetrics.com/v1/'
    TOKEN = None

    def __init__(self, token):
        self.TOKEN = token

    def __get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.TOKEN),
            'Accept': 'application/json'
        }

    def __get(self, url, **params):
        full_url = urljoin(self.BASE_URL, url)
        headers = self.__get_headers()

        r = requests.get(full_url, headers=headers, params=params)
        if r.status_code == 200:
            return r.json()
        raise BaremetricsException(r.content)

    def __post(self, url, data):
        full_url = urljoin(self.BASE_URL, url)
        headers = self.__get_headers()

        r = requests.post(full_url, headers=headers, data=data)
        if r.status_code == 200:
            return r.json()
        raise BaremetricsException(r.content)

    def __put(self, url, data):
        full_url = urljoin(self.BASE_URL, url)
        headers = self.__get_headers()

        r = requests.put(full_url, headers=headers, data=data)
        if r.status_code == 200:
            return r.json()
        raise BaremetricsException(r.content)

    def __delete(self, url):
        full_url = urljoin(self.BASE_URL, url)
        headers = self.__get_headers()

        r = requests.delete(full_url, headers=headers)
        if r.status_code == 200:
            return r.json()
        raise BaremetricsException(r.content)

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

    def update_plan(self, source_id, plan_id, name):
        return self.__put('{}/plans/{}'.format(source_id, plan_id), data={'name': name})
