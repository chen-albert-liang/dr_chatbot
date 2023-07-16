# %%
from bs4 import BeautifulSoup
import requests
import re
import json


def extract_links_from_webpage(url):
    # Send a get request to the webpage
    response = requests.get(url)

    # Make sure the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all 'a' tags and get their href attributes
        links = [a.get("href") for a in soup.find_all("a", href=True)]

        return links


# %%
def extract_text_from_webpage(url):
    # Send a get request to the webpage
    response = requests.get(url)

    # Make sure the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all text in the page
        # page_text = soup.get_text()
        page_text = [p.get_text() for p in soup.find_all("p")]

        # remove empty strings and \xa0'
        page_text = [p for p in page_text if p != ""]
        page_text = [p for p in page_text if p != "\xa0"]

        return page_text


# %% Haney Gyn Blogs
# blog_url = "https://haneygyn.com/blog/"  # replace this with your URL

# blog_urls = extract_links_from_webpage(blog_url)

# # Drop dupilcated links
# blog_urls = list(set(blog_urls))

# # Remove elemnts that are not links from haneygyn.com
# blog_urls = [url for url in blog_urls if "haneygyn.com" in url]

# # Extract the text from each blog post and store it in a json file
# haneygyn_blog = {}
# i = 0
# for url in blog_urls:
#     blog_text = extract_text_from_webpage(url)
#     haneygyn_blog[i] = blog_text
#     i += 1

# # Save the blog text in haneygyn_blog to a json file
# haneygyn_blog_json = json.dumps(haneygyn_blog)

# with open("haneygyn_blog.json", "w") as f:
#     f.write(haneygyn_blog_json)


# %% Frequently Asked Questions
faq_url = "https://www.menopause.org/for-women/expert-answers-to-frequently-asked-questions-about-menopause"  # replace this with your URL

faq_urls = extract_links_from_webpage(faq_url)

# Drop dupilcated links
faq_urls = list(set(faq_urls))

# Remove elemnts that are not links starting with for-women/expert-answers-to-frequently-asked-questions-about-menopause
faq_strings = "/for-women/expert-answers-to-frequently-asked-questions-about-menopause"

faq_urls = [url for url in faq_urls if url.startswith(faq_strings)]

# %%
# Extract the text from each blog post and store it in a json file
haneygyn_faqs = {}
i = 0
for url in faq_urls:
    faq_text = extract_text_from_webpage("https://www.menopause.org/" + url)
    haneygyn_faqs[i] = faq_text
    i += 1

# Save the blog text in haneygyn_blog to a json file
haneygyn_faqs_json = json.dumps(haneygyn_faqs)

with open("./haney_knowledge_base/faqs.json", "w") as f:
    f.write(haneygyn_faqs_json)

# %%
