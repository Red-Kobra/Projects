import requests

try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
 
# to search
query = "inurl:php?id=1"
 
for j in search(query, num_results=5, sleep_interval=5):
    print(j)