import requests

def get_follower_count(username):
    api_url = f'https://snailshare-backend.glitch.me/api/users/getFollowerCount?username={username}'

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            follower_count = int(response.text)
            return follower_count
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def id_to_name(args):
    api_url = f'https://snailshare-backend.glitch.me/api/pmWrapper/getProject?id={args["WHO"]}'

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            json_data = response.json()
            return json_data.get('name', '')
        else:
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def id_to_owner(args):
    api_url = f'https://snailshare-backend.glitch.me/api/pmWrapper/getProject?id={args["WHO"]}'

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            json_data = response.json()
            return json_data.get('author', {}).get('username', '')
        else:
            return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
