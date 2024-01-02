# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal
from typing import TypeAlias


SubjectClaimType: TypeAlias = Literal[
    'birthdate',
    'email',
    'family_name',
    'gender',
    'given_name',
    'middle_name',
    'name',
    'nickname',
    'phone_number',
]