"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import yaml
from inmanta_plugins.std import get_file_content

from inmanta.plugins import Context, plugin


@plugin
def load(path: "string", ctx: Context) -> "dict":
    """
    Parse the yaml found in the file at 'path' into a dictionary

    The path is according to the convention for std::source and std::file
    """
    return yaml.safe_load(get_file_content(ctx, "files", path))


@plugin
def loads(content: "string") -> "dict":
    """
    Parse the yaml found in `content` into a dictionary
    """
    return yaml.safe_load(content)
