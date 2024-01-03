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


from mybody_api_client.sections.base import RequestTypes, BaseSection


class Permission(BaseSection):
    prefix = 'permissions'

    async def get(self, id_str: str):
        path = '/get'
        response = await self.request(
            type_=RequestTypes.GET,
            path=path,
            token_required=False,
            parameters={
                'id_str': id_str,
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

    async def create(self, id_str: str, name: str):
        path = '/create'
        response = await self.request(
            type_=RequestTypes.POST,
            path=path,
            parameters={
                'id_str': id_str,
                'name': name,
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

