from django.shortcuts import render
import openai
from django.http import JsonResponse

# Configure your OpenAI API key
import random
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, Template

openai.api_key = "sk-proj-Zyt8nRKVCYy9bBDhFU1KT3BlbkFJJt8SYw7XW57rCAtzSxqs"
import requests
import json
from django.views.decorators.csrf import csrf_exempt


def generate_speech(request):
    message = ""
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        print("user_input", user_input)
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}",
        }
        data = {
            "model": "gpt-4.0",
            "messages": [
                {"role": "system", "content": user_input},
                {"role": "user", "content": "Hello!"},
            ],
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            print(response.json())  # Print or process the response JSON
        else:
            print(f"Error: {response.status_code}, {response.text}")
        message = response.json()["choices"][0]["message"]["content"]

    return render(
        request, "speech.html", {"completion": "null" if not message else message}
    )


def homepage(request):
    return render(request, "homepage.html")


def generate_translation(request):
    # API endpoint for GPT-3 text completion with Davinci engine
    url = "https://api.openai.com/v1/engines/davinci/completions"

    # Example prompt for text completion
    prompt = "Translate the following English text into French:"

    # Define headers including Authorization with your API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    # Define data payload with required parameters
    data = {
        "prompt": prompt,
        "max_tokens": 50,  # Adjust based on your needs
    }

    # Send POST request to OpenAI API
    try:
        response = requests.post(url, headers=headers, json=data)
        completion_text = response
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            print(response.json())  # Print or process the response JSON
        else:
            print(f"Error: {response.status_code}, {response.text}")
        return render(
            request,
            "speech.html",
            {"completion": "null" if not completion_text else completion_text},
        )
    except requests.exceptions.RequestException as e:
        print(
            f"Request error: {e}"
        )  # Handle any exceptions that occur during the request


def aram_generator(request):
    # Function to get all champion information
    def get_all_champions():
        # URL for the latest champion data
        url = "https://ddragon.leagueoflegends.com/cdn/14.15.1/data/en_US/champion.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code, response.text

    def generate_teams(players):
        # if len(players) != 8:
        #     raise ValueError("The number of players must be exactly 8.")

        # Shuffle the list of players randomly
        random.shuffle(players)

        # Split the players into two teams
        team1 = players[:team_size]
        team2 = players[team_size:]

        return ", ".join(team1), ", ".join(team2)

    def generate_teams_from_set(numbers_set, team_size):
        if len(numbers_set) < team_size * 2:
            raise ValueError("The set size is too small for the desired team sizes.")

        # Convert the set to a list for shuffling
        numbers_list = list(numbers_set)

        # Shuffle the list of numbers randomly
        random.shuffle(numbers_list)

        # Split the shuffled list into two teams
        team1 = numbers_list[:team_size]
        team2 = numbers_list[team_size : team_size * 2]

        return team1, team2

    players = [
        "zb",
        "suancai",
        "tong",
        "haitao",
        "mengge",
        "yiheng",
        "xiajiao",
        "yimeng",
    ]
    team_size = int(len(players) / 2)
    champ_number = 18
    if request.method == "POST":
        players = [
            s for s in request.POST.get("players").replace("\n", "").split("\r") if s
        ]
        team_size = int(len(players) / 2)
        print(players)
        print(team_size)
        # Process the input (e.g., save to database, perform calculations, etc.)

    # Example usage
    champions_data = get_all_champions()
    key_to_champion = dict()
    if isinstance(champions_data, dict):
        for champ_id, champ_info in champions_data["data"].items():
            # print(f"ID: {champ_id}, Name: {champ_info['name']}, Title: {champ_info['title']}")
            key_to_champion[champ_info["key"]] = champ_id
        champ_number = min(
            int(request.POST.get("champ_number")) if request.method == "POST" else 18,
            int(len(champions_data["data"].items()) / 2) if champions_data else 18,
        )

    else:
        print(f"Failed to fetch data: {champions_data}")

    team1, team2 = generate_teams(players)
    team1_champions, team2_champions = generate_teams_from_set(
        key_to_champion.keys(), champ_number
    )
    team1_champions, team2_champions = [
        key_to_champion[str(key)] for key in team1_champions
    ], [key_to_champion[str(key)] for key in team2_champions]
    return render(
        request,
        "aram.html",
        {
            "current_version": "14.15.1",
            "champ_number": champ_number,
            "team1": team1,
            "team2": team2,
            "team1_champions": team1_champions,
            "team2_champions": team2_champions,
            "players": "\r".join(players),
            "team_size": len(team1),
        },
    )
