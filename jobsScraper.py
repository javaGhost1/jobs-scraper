import sys
import requests
import bs4
import json
import pandas as pd

def scrape_for_jobs():
    base_url = 'https://www.brightermonday.co.ke/jobs'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36'
    }
    try:
        res = requests.get(base_url, headers=headers)
        res.raise_for_status()

        jobs_list = []
        soup = bs4.BeautifulSoup(res.content, 'html.parser')
        jobs_postings = soup.find_all('div', class_='mx-5 md:mx-0 flex flex-wrap col-span-1 mb-5 bg-white rounded-lg border border-gray-300 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-gray-500')
        for card in jobs_postings:
            # Extract job title
            job_title = card.find('p', class_='text-lg font-medium break-words text-link-500').text.strip()
            # Extract company name
            company_name = card.find('a', class_='text-link-500').text.strip()
           
            # Extract location
            location = card.find('span', class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide').text.strip()
           
            # Extract job function
            job_function = card.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').text.strip()
            # Extract job description
            job_desc = card.find('p', class_='text-sm font-normal text-gray-700 md:text-gray-500 md:pl-5').text.strip()
            # Extract posting date
            posting_date = card.find('p', class_='ml-auto text-sm font-normal text-gray-700 text-loading-animate').text.strip()

            jobs = {
                'job_title': job_title,
                'company_name': company_name,
               
                'location': location,
                'job_function': job_function,
                'job_desc': job_desc,
                'posting_date': posting_date                
            }

            jobs_list.append(jobs)
            print("saving", jobs['job_title'])


        # Create a DataFrame
        # df = pd.DataFrame(jobs_list)
        # save as a csv
        # df.to_csv('jobs_data.csv', index=False)
        print(len(jobs_list), "total jobs")
        return json.dumps(jobs_list)
       
    except requests.RequestException as e:
        print("Error fetching website:", e)

if __name__ == "__main__":
    jobs = scrape_for_jobs()
    if jobs:
        with open('jobs_data.json', 'w') as f:
            f.write(jobs)

        print('Jobs data saved as a json file')
