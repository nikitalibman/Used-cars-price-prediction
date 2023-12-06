"""
In order to run this module we have to go to the website https://hidemy.io/en/proxy-list/
and select checkboxes Proxy types: 'HTTPS' and Anonymity: 'High' and click the button 'Show'.
Then we have to manually inspect the appeared table and copy the entire html element <table>.
The extracted html code we save into a txt file 'ip_html.txt'.
The result of this module returns a txt file 'proxies.txt' with all valid and fresh proxy servers
"""

from bs4 import BeautifulSoup

with open('ip_html.txt') as f:
    html = f.read()

#soup = BeautifulSoup(html, 'lxml')
soup = BeautifulSoup(html, 'html5lib')
ip_soup = soup.find_all('td')
ip_list = []
for el in ip_soup:
    ip_list.append(el.get_text())

filtered_list = []
# Iterate through each item in the original_list
for item in ip_list:
    has_alpha = False

    for char in item:
        if char.isalpha():
            has_alpha = True
            break

    if not has_alpha and item.strip():
        filtered_list.append(item)

joined = []

# Loop through the original list with a step of 2
# This way, we get every pair of consecutive elements
for i in range(0, len(filtered_list), 2):
    # Form a string by joining the current element and the next element with a colon
    pair = f'{filtered_list[i]}:{filtered_list[i + 1]}'

    # Add the formed pair to the 'joined' list
    joined.append(pair)

# Print the 'joined' list
with open('proxies.txt', 'w') as file:
    for item in joined:
        file.write(item + '\n')
