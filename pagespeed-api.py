import requests
import os

# Documentation: https://developers.google.com/speed/docs/insights/v5/get-started
# JSON paths: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed

# Populate 'pagespeed.txt' file with URLs to query against API.

with open('pagespeed.txt') as pagespeedurls:
    download_dir = 'pagespeed-results.csv'
    
    if os.path.exists(download_dir):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not
    
    file = open(download_dir, append_write)
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]

    if append_write == 'w':
        columnTitleRow = "Date Time, URL, First Contentful Paint, First Interactive\n"
        file.write(columnTitleRow)

    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file

    for line in content:
        # If no "strategy" parameter is included, the query by default returns desktop data.
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}&strategy=mobile'
        print(f'Requesting {x}...')

        r = requests.get(x, verify = False)
        final = r.json()

        try:
            timestamp = final['analysisUTCTimestamp']
            DATETIME = f'DATETIME ~ {timestamp}' 
            urlid = final['id']
            split = urlid.split('?') # This splits the absolute url from the api key parameter
            urlid = split[0] # This reassigns urlid to the absolute url
            ID = f'URL ~ {urlid}'
            ID2 = str(urlid)
            urlfcp = final['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
            FCP = f'First Contentful Paint ~ {str(urlfcp)}'
            FCP2 = str(urlfcp)
            urlfi = final['lighthouseResult']['audits']['interactive']['displayValue']
            FI = f'First Interactive ~ {str(urlfi)}'
            FI2 = str(urlfi)

        except KeyError:
            print(f'<KeyError> One or more keys not found {line}.')

        try:
            row = f'{timestamp},{ID2},{FCP2},{FI2}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')

        try:
            print(DATETIME)
            print(ID) 
            print(FCP)
            print(FI)
            #print(final)

        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')

    file.close()
