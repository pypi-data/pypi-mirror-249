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


class Account(BaseSection):
    prefix = 'accounts'

    async def get(self, id_: int = None):
        path = '/get'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id': id_,
            },
        )
        return response

    async def get_additional(self):
        path = '/additional/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
        )
        return response

    async def search(self, id_: int = None, username: str = None, page: int = None):
        path = '/search'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id': id_,
                'username': username,
                'page': page,
            },
        )
        return response

    async def create(
            self,
            username: str,
            password: str,
            firstname: str,
            lastname: str,
            country: str,
            language: str,
            timezone: str,
            currency: str,
            surname: str = None,
    ):
        path = '/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            token_required=False,
            parameters={
                'username': username,
                'password': password,
                'firstname': firstname,
                'lastname': lastname,
                'surname': surname,
                'country': country,
                'language': language,
                'timezone': timezone,
                'currency': currency,
            },
        )
        return response

    async def check_username(self, username: str):
        path = '/username/check'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'username': username,
            }
        )
        return response

    async def get_service(self, id_: int):
        path = '/services/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'id': id_,
            }
        )
        return response

    async def services_get_list(self):
        path = '/services/list/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
        )
        return response

    async def create_service(
            self,
            account_username: str,
            service_id_str: str,
            answers: str,
            state: str,
    ):
        path = '/services/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'account_username': account_username,
                'service_id_str': service_id_str,
                'answers': answers,
                'state': state,
            }
        )
        return response

    async def update_service(self, id_: int, answers: str, state: str):
        path = '/services/update'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_': id_,
                'answers': answers,
                'state': state,
            }
        )
        return response

    async def delete_service(self, id_: int):
        path = '/services/delete'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_': id_,
            }
        )
        return response
