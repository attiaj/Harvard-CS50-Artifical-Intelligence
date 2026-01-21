from ctypes import sizeof
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution_dict = dict()
    num_outgoing_links = len(corpus[page])

    # If the page is an outgoing link from the current page, it gets the probability from following a link 
    # (damping_factor divided among outgoing links) plus the probability from random selection
    if num_outgoing_links != 0: 
        for page_name in corpus:
            if page_name in corpus[page]:
                distribution_dict[page_name] = (damping_factor / num_outgoing_links) + (1 - damping_factor) / len(corpus)
        # if page is not an outgoing link from current page, it only gets the probability from random selection
            else:
                distribution_dict[page_name] = (1 - damping_factor) / len(corpus)
    # if no outgoing links, each page has equal chance of selection
    else:
        for page_name in corpus:
            distribution_dict[page_name] = 1 / len(corpus)
    
    return distribution_dict



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Keep track of num times each page is visited with a dictionary
    num_times_visted = dict()
    for page in corpus:
        num_times_visted[page] = 0

    # First sample is a random selection from all pages
    current_page = random.choice(list(corpus))
    current_sample_num = 1
    num_times_visted[current_page] += 1

    # Loop to get 'n' total samples, including first random sample
    while (current_sample_num < n):
        current_page_transition_model = transition_model(corpus, current_page, damping_factor)
        possible_next_pages = list(current_page_transition_model.keys())
        next_page_probabilites = list(current_page_transition_model.values())

        # Next page is a random choice from the transition model, calculate weights using transition_model function,
        # then use random.choices to make a weighted random choice
        current_page = random.choices(possible_next_pages, weights=next_page_probabilites)[0]
        num_times_visted[current_page] += 1

        current_sample_num += 1
    
    # Each page's pagerank is the proportion of total samples where the page was visited
    pageranks = dict()
    for page in corpus:
        pageranks[page] = num_times_visted[page] / sum(num_times_visted.values())
    
    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    convergence_factor = 0.001
    total_num_pages = len(corpus)
    old_pageranks = dict()
    for page in corpus:
        old_pageranks[page] = 1 / total_num_pages
    
    new_pageranks = dict()
    convergence_check_passed = False

    # Loop until the new pageranks are within 0.001 of the old pageranks
    while(convergence_check_passed == False):
        for pages in corpus:
            summation_term = 0
            incoming_links = []

            # Create a list of pages that link to the current page, pages with no outgoing links are treated as linking to all pages, include those as well
            for page in corpus:
                if pages in corpus[page] or len(corpus[page]) == 0:
                    incoming_links.append(page)

            # Create summation term using formula described, while setting "NumLinks" = total number of pages if there are no outgoing links
            for page in incoming_links:
                if len(corpus[page]) != 0:
                    summation_term += old_pageranks[page] / len(corpus[page])
                else:
                    summation_term += old_pageranks[page] / len(corpus)
            
            # Use a separate dictionary to hold new pageranks, to compare to the old pageranks, checking if values have converged enough
            new_pageranks[pages] = ((1 - damping_factor) / total_num_pages) + damping_factor * summation_term 

        convergence_check_passed = True
        for page in new_pageranks:
            if abs(new_pageranks[page] - old_pageranks[page]) > convergence_factor:
                convergence_check_passed = False

        old_pageranks = new_pageranks.copy()
    
    return new_pageranks


if __name__ == "__main__":
    main()
