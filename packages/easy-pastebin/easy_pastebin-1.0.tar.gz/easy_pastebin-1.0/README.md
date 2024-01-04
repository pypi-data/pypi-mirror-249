# My Pastebin Python Library

## Functions

### `get_paste_content_withApiKey`  
Gets raw text from a Pastebin with your API key.  
**Usage:** `get_paste_content_withApiKey(my_api_key, paste_id)`

### `set_pastebin_apiKey`  
Sets your Pastebin API key.  
**Usage:** `set_pastebin_apiKey(my_api_key)`

### `get_paste_content`  
Gets raw text from a Pastebin without your API key. Provide it using the `set_pastebin_apiKey` function.  
**Usage:** `get_paste_content(paste_id)`