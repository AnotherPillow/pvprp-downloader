import bs4, requests, os

url = input('Enter URL: ')

res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')
script = soup.find_all('script')[-1]

#get string between ".attr("href","assets/packs and ");"
partial_link = script.string.split('.attr("href","assets/packs')[1].split('")')[0]
partial_link = partial_link.split('?')[0]

link = f'https://pvprp.com/assets/packs{partial_link}'
filename = link.split('/')[-1]

download = input('Download? (y/n): ').strip().lower().startswith('y')

if download:
    res = requests.get(link)
    res.raise_for_status()

    #get windows username
    
    if os.name == 'nt':
        username = os.getlogin()
        os.chdir(f'C:\\Users\\{username}\\Downloads')

    with open(filename, 'wb') as f:
        f.write(res.content)
        f.close()

    print(f'Downloaded {filename} to {os.getcwd()}')
else:
    print(f'Direct link: {link}')