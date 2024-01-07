Disid
=====
An Integer ID Disguiser to make your values look more professional.

Transform plain incrementing ids:
```
https://example.com/blogpost/1
https://example.com/blogpost/2
https://example.com/blogpost/3
https://example.com/blogpost/4
```
Into random looking values befitting of a popular website:
```
https://example.com/blogpost/WxYRW
https://example.com/blogpost/2zfow
https://example.com/blogpost/SyyUZ
https://example.com/blogpost/EIrPp
```

The process is reversable and does not need access to a database. A optional static key file can be distributed among all of the processes that need to convert between a Disid id and a numerical value.

Example
=======

```python
from typing import List
import os
import keytools
import disid

def load_key(file: str) -> List[str]:
    if os.path.exists(file):
        with open(file, 'rb') as f:
            key = f.read()
    else:
        with open(file, 'wb') as f:
            key = keytools.generate_key(5)
            f.write(key)

    return keytools.convert_key_to_character_lists(key)

def main():
    character_list = load_key("my_keyfile.key")
    print(disid.uint_to_id_v3(1, character_list))
    print(disid.uint_to_id_v3(2, character_list))
    print(disid.uint_to_id_v3(3, character_list))
    print(disid.uint_to_id_v3(4, character_list))
```

Security
========
This should not be considered cryptographically secure. Do not use Disid to expose values to a user that should otherwise not be exposed. Only use Disid as a cosmetic layer on top of your already public values.

