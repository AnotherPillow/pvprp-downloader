import bs4, requests, os
url_list = []

while True:
    #split with & to remove search part of url when dragging to terminal
    url = input('Enter URL(leave blank to download): ').split('&')[0]

    if url == "":
        break

    #create list of urls to download in bulk
    url_list.append(url)

if len(url_list) == 0:
    print("No packs to download")
    exit()


#get windows username
if os.name == 'nt':
    username = os.getlogin()
    os.chdir(f'C:\\Users\\{username}\\Downloads')
else:
    os.mkdir("./output")
    os.chdir("./output")

# make the script download the pack by default
download = input(f'Download {len(url_list)} packs? (Y/n): ').strip().lower().startswith('n')

for i in range(0, len(url_list)):
    # prevent crash from a wrong url
    try:
        res = requests.get(url_list[i])
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        script = soup.find_all('script')[-1]

        #get string between ".attr("href","assets/packs and ");"
        partial_link = script.string.split('.attr("href","assets/packs')[1].split('")')[0]
        partial_link = partial_link.split('?')[0]

        link = f'https://pvprp.com/assets/packs{partial_link}'
        filename = link.split('/')[-1]

        # defaults to downloading
        if download:
            print(f'Direct link: {link}')
        else:
            res = requests.get(link)
            res.raise_for_status()


            with open(filename, 'wb') as f:
                f.write(res.content)
                f.close()

            print(f'Downloaded {filename} to {os.getcwd()}')
    except:
        print(f"Invalid URL {url_list[i]}")

