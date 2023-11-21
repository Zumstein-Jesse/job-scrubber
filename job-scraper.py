import requests
from bs4 import BeautifulSoup
import os

url = "https://www.riotgames.com/en/work-with-us"

def fetch_current_jobs(url):
    """Returns list of all jobs listed on website
    
    :param url: website containing job listings
    :type url: string
    :rtype current_jobs: string
    :return current_jobs: formatted string of jobs    
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    current_jobs = set()

    for li in soup.select("ul.job-list__body li.job-row"):
        title = " ".join(li.select_one("div.job-row__col--primary").text.strip().split())
        department = " ".join(li.select("div.job-row__col--secondary")[0].text.strip().split())
        project = " ".join(li.select("div.job-row__col--secondary")[1].text.strip().split())
        location = " ".join(li.select("div.job-row__col--secondary")[2].text.strip().split())
        
        job_detail = f"Title: {title}\nDepartment: {department}\nProject: {project}\nLocation: {location}"
        current_jobs.add(job_detail)
        
    return current_jobs


def read_jobs_from_file(filename):
    """Reads through local file and returns jobs 
    
    :param filename: file to be read
    :type filename: _io.TextIOWrapper
    :rtype jobs: set
    :return jobs: formatted set of jobs    
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()[2:]  # Skip the first 2 lines (title and a blank line)
            jobs = set()
            for i in range(0, len(lines), 5):  # Step of 5 because each job has 4 lines + 1 blank line
                job = "".join(lines[i:i+4]).strip()
                jobs.add(job)
        return jobs
    except FileNotFoundError:
        return set()


def write_jobs_to_file(filename, jobs, title):
    """Writes jobs to filename arg
    
    :param filename: file to be read
    :type filename: _io.TextIOWrapper
    :param jobs: formatted set of jobs  
    :type jobs: set
    :param title: Title at the top of the document
    :type title: string   
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(title + "\n\n")  # Write the title and add a blank line
        for job in jobs:
            f.write(job + "\n\n")  # Each attribute on its own line, extra line after each job


if __name__ == "__main__":
    # Get desktop path
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive//Desktop')

    # File paths
    all_jobs_file = os.path.join(desktop, 'RiotJobs.txt')
    new_jobs_file = os.path.join(desktop, 'RiotJobsNew.txt')
    all_jobs_ever_file = os.path.join(desktop, 'AllJobsEver.txt')

    # Read existing jobs
    existing_jobs = read_jobs_from_file(all_jobs_file)
    
    # Read all jobs ever seen
    all_jobs_ever = read_jobs_from_file(all_jobs_ever_file)

    # Fetch current jobs
    current_jobs = fetch_current_jobs(url)

    # Identify new jobs based on all jobs ever seen
    new_jobs = current_jobs - all_jobs_ever
    
    # Update the record of all jobs ever seen
    all_jobs_ever |= new_jobs
    write_jobs_to_file(all_jobs_ever_file, all_jobs_ever, "All Jobs Ever Seen")

    # Update existing jobs
    write_jobs_to_file(all_jobs_file, current_jobs, "Riot Games Current Jobs")

    # Write only new jobs to RiotJobsNew.txt
    write_jobs_to_file(new_jobs_file, new_jobs, "Riot Games New Jobs")