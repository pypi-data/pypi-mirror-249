#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from mybody_api_client.sections.base import BaseSection, RequestTypes


class Service(BaseSection):
    prefix = 'services'

    async def get(self, id_: str):
        path = '/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'id_str': id_,
            },
        )
        return response

    async def get_list(self):
        path = '/list/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
        )
        return response

    async def create(self, id_str: str, name: str, questions: str):
        path = '/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_str': id_str,
                'name': name,
                'questions': questions,
            },
        )
        return response

    async def update(self, id_str: str, name: str = None, questions: str = None):
        path = '/update'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_str': id_str,
                'name': name,
                'questions': questions,
            },
        )
        return response

    async def delete(self, id_str: str):
        path = '/delete'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_str': id_str,
            },
        )
        return response

    async def get_costs_list(self, service_id_str: str):
        path = '/costs/list/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            parameters={
                'service_id_str': service_id_str
            },
            token_required=False,
        )
        return response

    async def create_cost(self, service_id_str: str, currency_id_str: str, cost: float):
        path = '/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'service_id_str': service_id_str,
                'currency_id_str': currency_id_str,
                'cost': cost,
            },
        )
        return response

    async def update_cost(self, id_: int, cost: float):
        path = '/update'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_': id_,
                'cost': cost,
            },
        )
        return response

    async def delete_cost(self, id_: int):
        path = '/delete'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_': id_,
            },
        )
        return response
