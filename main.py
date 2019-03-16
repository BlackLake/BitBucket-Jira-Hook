from flask import Flask, request
import json
import requests


def webhook_exist():
    url = "http://localhost:8080/rest/webhooks/1.0/webhook"

    payload = "{\n\"name\": \"auto creator script\",\n\"url\": \"http://127.0.0.1:5000/\",\n\"events\": [\n  \"project_created\"\n],\n\"excludeBody\" : false\n}"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic QmxhY2tMYWtlOjA1MzI3MzIwNjUw",
        'cache-control': "no-cache",
        'Postman-Token': "586fddcc-bbff-478e-b783-515995137617"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    for hook in response.json():
        if hook['name'] == "auto creator script":
            return True
    return False


def post_create_webhook():
    if not webhook_exist():
        url = "http://localhost:8080/rest/webhooks/1.0/webhook"

        payload = "{\n\"name\": \"auto creator script\",\n\"url\": \"http://127.0.0.1:5000/\",\n\"events\": [\n  \"project_created\"\n],\n\"excludeBody\" : false\n}"
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Basic QmxhY2tMYWtlOjA1MzI3MzIwNjUw",
            'cache-control': "no-cache",
            'Postman-Token': "905cb783-7e9c-4ebe-9e5d-3f998dbf6884"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        print("webhook created :", response.json())
    else:
        print("webhook exists")


def get_jira_projects():
    url = "http://127.0.0.1:8080/rest/api/2/project"

    payload = ""
    headers = {
        'Authorization': "Basic QmxhY2tMYWtlOjA1MzI3MzIwNjUw",
        'cache-control': "no-cache",
        'Postman-Token': "f76a0924-a2d3-41ba-806f-9f6cfa30ff55"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    return response.json()


def post_bitbucket_project(key, name):
    url = "http://localhost:7990/rest/api/1.0/projects"

    payload = '{"key":"' + key + '","name":"' + name + '"}'
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic QmxhY2tMYWtlOjA1MzI3MzIwNjUw",
        'cache-control': "no-cache",
        'Postman-Token': "e3c1b86c-33e8-41df-9a1c-b73e191fd6dd"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print("bitbucket project create request sent :", response.json())


post_create_webhook()

for jira in get_jira_projects():
    post_bitbucket_project(jira['key'], jira['name'])

app = Flask(__name__)


@app.route('/', methods=['POST'])
def jira_project_created():
    data = json.loads(request.data)
    print("jira project created :", data)
    key = data['project']['key']
    name = data['project']['name']
    post_bitbucket_project(key, name)
    return "bitbucket project create request sent. key:" + key + "name : " + name


if __name__ == '__main__':
    app.run()
