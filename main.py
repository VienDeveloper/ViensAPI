from fastapi import FastAPI 
from translate import Translator
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import phonenumbers
from phonenumbers import carrier

app = FastAPI(version='1.0.0', description='Just some of my API\'s...<br>By using this api you agree to follow the <a href="/tos/">TOS</a>' ,title='Vien\'s API collection\'s', docs_url=None, redoc_url='/docs', contact={'email': 'vien@courvix.com'}, terms_of_service='/tos/', license_info={'name': ' GPL-3.0 license', 'url': 'https://www.gnu.org/licenses/gpl-3.0.en.html'})

@app.get('/',include_in_schema=False)
async def home():
    return RedirectResponse(url="/docs")

@app.get('/api/translate/', description='''
Translate a text using MyMemory.
Use the country name or use ISO 639-1 for, \'from_lang\', \'to_lang\'
''')
async def translate( text: str,  to_lang: str, from_lang: str):
    """_summary_

    Args:
        text (str): the text thats gonna get transated
        to_lang (str): The destined lang
        from_lang (str): original language of the text

    Returns:
        _type_: json
    """    
    translator= Translator(to_lang=to_lang, from_lang=from_lang, email='viendev.py@gmail.com')
    translation = translator.translate(text)
    return {"details": 'Success', "to_lang": to_lang, 'from_lang': from_lang, 'textOriginal': text, 'textTranslated': translation}

@app.get('/api/validatenumber/', description='''
Checks if the phone number is valid using Google's libphonenumber library.
Will also provide information about the user. <a href="https://en.wikipedia.org/wiki/E.164" ><b>Use E.164 Format </b></a> (example +1 4151231234). MAKE SUE TO ENCODE THE USR AND REPLACE + WITH %2B

''')
async def phonevalidate(pnumber: str):
    try:
        number = phonenumbers.parse(pnumber, None)
        carriers = carrier.name_for_number(number, "en")

        valid = phonenumbers.is_valid_number(number)
        if valid == True:
            return {'countrycode': number.country_code, 'natitonal_number': number.national_number, 'valid': True, 'carrier': carriers}
        else:
            return {'valid': False, 'countrycode': None, 'national_number': None, 'carrier': None}
    except phonenumbers.phonenumberutil.NumberParseException as r:
        return {'details': f'Invalid number, {r}'}
@app.get('/tos/', include_in_schema=False)
async def tos():    
    html_content = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Terms of Service - Vien's API Collection</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  </head>
  <body>
    <div class="container my-5">
      <h1 class="text-center">Terms of Service - Vien's API Collection</h1>
      <p>Welcome to Vien's API Collection, a collection of APIs available at vienapi.deta.dev.</p>
      <p>By using our APIs, you agree to the following terms and conditions:</p>
      <ol>
        <li>
          <p>The APIs provided by Vien's API Collection are intended for legitimate use only. You may not use our APIs in any way that violates the law or any third-party rights, or in any way that is deceptive or malicious. This includes, but is not limited to, using our APIs for spamming, phishing, hacking, or any other illegal activity.</p>
        </li>
        <li>
          <p>Vien's API Collection reserves the right to modify or discontinue any of our APIs without notice. We will not be liable for any harm caused by such changes. Additionally, we may impose usage limits on our APIs to ensure fair and responsible use by all users.</p>
        </li>
        <li>
          <p>You may not use our APIs in any manner that could overburden, disable, or damage our servers or network infrastructure. You also may not use our APIs to run any kind of automation that would excessively or needlessly increase API usage. This includes, but is not limited to, using scripts or other tools that make multiple API requests per second or make excessive use of our resources.</p>
        </li>
        <li>
          <p>Vien's API Collection is not responsible for any harm that may result from the use of our APIs. This includes, but is not limited to, harm to your computer system, loss of data, or other harm. You agree to use our APIs at your own risk. Additionally, we do not guarantee the accuracy or completeness of the data provided through our APIs.</p>
        </li>
        <li>
          <p>You agree to indemnify and hold harmless Vien's API Collection and its owners, employees, agents, and affiliates from and against any claims, damages, losses, liabilities, and expenses arising from your use of our APIs.</p>
        </li>
        <li>
          <p>These terms and conditions shall be governed by and construed in accordance with the laws of the country in which the API servers are located. Any legal action arising from or in connection with these terms and conditions or the use of our APIs must be brought in the courts of that country.</p>
        </li>
      </ol>
      <p>These terms and conditions may be updated at any time, and your continued use of our APIs after any changes</p>

    '''
    return HTMLResponse(content=html_content, status_code=200)