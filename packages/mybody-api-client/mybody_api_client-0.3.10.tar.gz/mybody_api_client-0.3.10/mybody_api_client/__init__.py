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


from .sections import Permission
from .sections import Account
from .sections import Text
from .sections import Service
from .sections import Article
from .sections import Country
from .sections import Currency
from .sections import Language
from .sections import ServiceNotification
from .sections import Role
from .sections import Session
from .sections import Timezone
from .sections import Product
from .sections import Exercise
from .sections import Training
from .sections import Meal


sections = [
    Account,
    Article,
    Country,
    Currency,
    Language,
    ServiceNotification,
    Role,
    Service,
    Session,
    Text,
    Timezone,
    Product,
    Training,
    Exercise,
    Permission,
    Meal,
]


class MyBodyApiClient:
    account: Account
    article: Article
    country: Country
    currency: Currency
    language: Language
    notification_service: ServiceNotification
    role: Role
    service: Service
    session: Session
    text: Text
    timezone: Timezone
    product: Product
    training: Training
    exercise: Exercise
    permission: Permission
    meal: Meal

    def __init__(self, token: str = None):
        for section in sections:
            exec(f'self.{section.__name__.lower()} = section(token=token)')
