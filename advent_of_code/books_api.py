user_id = 112951405275631413697
access_token = "ya29.a0AXooCguACsO0p5GDgsvIXraBjQwmu1g8hnrnGvH8LeOlvaHvCydGAldam8Rq7vagX5YxtBcG1ymQk-ksCNmA5HVWvajoMQiGB4mLDT9xd4HGH8teRUhhUrNNG82ff3uy26pN_EM_cjzIo5WHN0s2Upsnrq5URZDh5wAPaCgYKAUwSARISFQHGX2MivdJQ4Ax-XodZgMI4cH8Apw0171"

import requests

api_key = "AIzaSyAh9CeXOUp1Xszo4Cxa1MrWa-i4Kig0daQ"  # Replace with your actual API key
access_token = access_token  # Replace with your actual access token
url = f"https://books.googleapis.com/books/v1/users/112951405275631413697/bookshelves?key={api_key}"

headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    bookshelves = response.json()
    # Process the bookshelves data (e.g., print it)
    print(bookshelves)
else:
    print(f"Error: {response.content}")


starF = lambda f: lambda args: f(*args)
