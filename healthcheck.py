# Healthcheck take home project
# Author: GitHub user myhreshannon

import datetime
import os.path
import requests
import sys
import time
from urllib.parse import urlparse
import yaml

def main():
    print("\nPlease press ctrl+c to exit this program\n")

    if len(sys.argv) == 1:
        print("Please provide a file path for HTTP endpoints you want to test")
        time.sleep(30)
        
    try:
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r') as file:
                input = yaml.safe_load(file)
        else:
            print("Invalid file path given. Exiting.")
            sys.exit(0)

        verbose = False
        if len(sys.argv) > 2:
            if sys.argv[2] == 'v':
                verbose = True

        results = {}

        while True:
            for endpoint in input:
                if verbose:
                    print(f"Testing {endpoint['url']}")

                #check to see if domain is in the results dictionary
                domain = urlparse(endpoint['url']).netloc
                if domain not in results:
                    results[domain] = {
                        'successful': 0,
                        'total': 0
                    }

                results[domain]['total'] += 1

                try:
                    endp_header = None
                    if 'headers' in endpoint.keys():
                        endp_header = endpoint['headers']

                    endp_body = None
                    if 'body' in endpoint.keys():
                        endp_body = endpoint['body']
                        
                    if 'method' not in endpoint.keys():
                        response = requests.get(endpoint['url'])
                    elif endpoint['method'] == 'GET':
                        response = requests.get(endpoint['url'], headers=endp_header)
                    elif endpoint['method'] == 'POST':
                        response = requests.post(endpoint['url'], headers=endp_header, data=endp_body)
                    elif endpoint['method'] == 'DELETE':
                        response = requests.delete(endpoint['url'], headers=endp_header, data=endp_body)
                    else:
                        print("Unhandled REST request type")

                    # Calculate latency in ms
                    latency = response.elapsed / datetime.timedelta(milliseconds=1)

                    if verbose:
                        print(f"Status code: {response.status_code}")
                        print(f"Latency: {round(latency)}ms")

                    # Check for a 2xx response code and latency under 500ms
                    if 200 >= response.status_code < 300:
                        if round(latency) < 500:
                            results[domain]['successful'] += 1
                            if verbose:
                                print("Success")

                except requests.exceptions.HTTPError as e:
                    print(f"HTTP error: {e}")
                except:
                    print("Error during request")

            # Print results after each test cycle
            for domain in results.keys():
                success_rate = 100 * (results[domain]['successful'] / results[domain]['total'])
                # Per instructions, round success_rate to nearest whole number
                print(f"{domain} has {round(success_rate)}% availability percentage")

            time.sleep(15)
        
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit(0)
    


if __name__ == '__main__':
    main()
