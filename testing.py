import requests

url = "https://api.gupshup.io/wa/app/2d6002e8-4662-43da-92d2-2523fdea7425/template"

payload = {
    "elementName": "auth_template__aaaaaa",
    "languageCode": "en",
    "vertical": "rytey",
    "templateType": "TEXT",
    "allowTemplateCategoryChange": True,
    "addSecurityRecommendation": True,
    "codeExpirationMinutes": 1,
    "content":"your ticket has been confirmed for"
}
headers = {
    "accept": "application/json",
    "apikey": "94d3874500a84f87cf63e14007f7cfa2",
    "content-type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)