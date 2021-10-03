# django-random-api
Free API With Random Features


### change api-key
```
method: PUT
url: https://salisganteng.pythonanywhere.com/api/change-api-key

mandatory parameter:
- api-key
```

### change password
```
method: PUT
url: https://salisganteng.pythonanywhere.com/api/change-password

mandatory parameters:
- api-key
- password (current password)
- new-password
```

### writing in a book
```
method: POST
url: https://salisganteng.pythonanywhere.com/api/write

mandatory parameters:
- api-key
- text
```

### text to image
```
method: POST
url: https://salisganteng.pythonanywhere.com/api/text2img

mandatory parameters:
- api-key
- text

optional parameters:
- bgColor (background color; rgba; default: 0,0,0,0)
- textColor (text color; rgba; default: 255,255,255,255)
- outlineColor (text outline color; rgba; default: 0,0,0,255)
```

### text to gif
```
method: POST
url: https://salisganteng.pythonanywhere.com/text2gif

mandatory parameters:
- api-key
- text
```

### wikipedia
```
method: GET
url: https://salisganteng.pythonanywhere.com/wikipedia

mandatory parameters:
- api-key
- text
```

### math
```
method: GET
url: https://salisganteng.pythonanywhere.com/math

mandatory parameter:
- api-key
```

# remove background image
```
method: POST
url: https://salisganteng.pythonanywhere.com/api/remove-bg

mandatory paramaters:
- api-key
- image (convert to base64)
```
