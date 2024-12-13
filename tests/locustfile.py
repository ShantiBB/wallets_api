from locust import HttpUser, between, SequentialTaskSet, task
import random


class ApiTest(SequentialTaskSet):

    @task(1)
    def create_item(self):
        token = '428d03f46300faacbe6d93ff2d2a3077fc823e86'
        self.client.headers.update(
            {'Authorization': f'Token {token}'}
        )
        data = {
            'operation_type': 'DEPOSIT',
            'amount': random.randint(10, 1000)
        }
        wallet_id = '73e11817-4174-4a4c-bc11-1673a9c9bcbe'
        absolute_url = f'/api/v1/wallets/{wallet_id}/operation/'
        self.client.post(absolute_url, json=data)

    @task(2)
    def get_items(self):
        token = '428d03f46300faacbe6d93ff2d2a3077fc823e86'
        self.client.headers.update(
            {'Authorization': f'Token {token}'}
        )
        absolute_url = '/api/v1/wallets/'
        self.client.get(absolute_url)

    @task(3)
    def get_item(self):
        token = '428d03f46300faacbe6d93ff2d2a3077fc823e86'
        self.client.headers.update(
            {'Authorization': f'Token {token}'}
        )
        wallet_id = '73e11817-4174-4a4c-bc11-1673a9c9bcbe'
        absolute_url = f'/api/v1/wallets/{wallet_id}/'
        self.client.get(absolute_url)


class UserBehavior(HttpUser):
    tasks = [ApiTest]
    wait_time = between(0.1, 0.5)
