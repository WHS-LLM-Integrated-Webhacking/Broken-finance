from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import openai
import datetime
import os
from .prompt import first_prompt_template, second_prompt_template
from flask import current_app
import jwt
import requests

google_api_key = os.environ["GOOGLE_API_KEY"] 
google_cse = os.environ["GOOGLE_CSE"]
openai_api_key = os.environ["OPENAI_API_KEY"]


def google_search(query, **kwargs):
    service = build("customsearch", "v1", developerKey=google_api_key)
    res = service.cse().list(q=query, cx=google_cse, **kwargs).execute()
    return res['items']

def fetch_website_content(url):
    admin_token = jwt.encode({
        'user_id': 1,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    headers = {'x-access-token': admin_token} # Gifts for hackers
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string if soup.title else 'No title found'
    content = soup.get_text() if soup.get_text() else 'No content found'

    return {
        'title': title,
        'content': content
    }

def service(command, user_id):
    command = command.split()
    admin_token = jwt.encode({
        'user_id': 1,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    headers = {'x-access-token': admin_token}

    def handle_transaction(command):
        user_account, transfer_account, amount = command[2:5]
        check = requests.get(f'http://127.0.0.1:5000/api/accounts/{user_account}/{user_id}/check', headers=headers)
        if check.status_code != 201:
            return "Invalid Account ID."
        data = {'account_id': user_account, 'dest_account': transfer_account, 'amount': amount}
        transaction = requests.post('http://127.0.0.1:5000/api/transactions/', json=data, headers=headers)
        if transaction.status_code != 201:
            return "Transaction failed."
        return f"Transaction Success! {user_account} => {transfer_account} (Amount: {amount})"

    def handle_add_account(command):
        if command[2] == "Failed":
            return f"Account add Failed. Reason: {command[3]}"
        account_name, account_type = command[2:4]
        data = {'account_name': account_name, 'account_type': account_type, 'user_id': user_id}
        add = requests.post('http://127.0.0.1:5000/api/accounts/admin-add', json=data, headers=headers)
        if add.status_code != 201:
            return "Account add failed."
        return f"Account Successfully added! Account name: {account_name}, Account type: {account_type}, Account ID: {add.json()['account_id']}"

    command_type = command[1]
    if command_type == 'Transaction':
        return handle_transaction(command)
    elif command_type == 'AddAccount':
        return handle_add_account(command)


def llm_web_retriever(name, question, user_id):
    now = datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S")
    openai.api_key = openai_api_key
    client = openai.OpenAI(api_key=openai.api_key)

    first_prompt = first_prompt_template.safe_substitute(now=now, question=question)
        
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": first_prompt},
            ],
        max_tokens=800
    )
    res1 = response.choices[0].message.content.split('\n')

    contents = {}
    service_resource = ""
    for context in res1:
        if context.startswith("None"): 
            continue

        match context.split(' ', 1):
            case ["127.0.0.1", _] | ["localhost", _] | ["web", _],:
                return {"response": "127.0.0.1, localhost, web에는 접속할 수 없어요!", "content": contents}

            case ["Access", url]:
                try: 
                    content = fetch_website_content(url)
                except: 
                    content = {'None': 'None'}
                contents = contents | content

            case ["Search", query]:
                search_results = google_search(query, num=3)
                search_content = []
                for result in search_results:
                    title = result.get('title')
                    link = result.get('link')
                    date = result.get('pagemap', {}).get('metatags', [{}])[0].get('og:updated_time', 'N/A')
                    search_content.append({'title': title, 'link': link, 'date': date})
                for item in search_content:
                    try: 
                        content = fetch_website_content(item['link'])
                    except: 
                        content = {'None': 'None'}
                    contents = contents | content

            case ["Service", _]:
                service_resource = service(context, user_id)
            
    contents = "\n".join([f"{key}: {value}" for key, value in contents.items()])
    second_prompt = second_prompt_template.safe_substitute(contents=contents, service_resource=service_resource, name=name, question=question)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": second_prompt},
            ],
        max_tokens=800
    )
    res2 = response.choices[0].message.content
    return {"response": res2}