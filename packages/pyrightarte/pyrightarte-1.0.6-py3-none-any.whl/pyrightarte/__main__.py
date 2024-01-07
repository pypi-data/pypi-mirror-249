from googlesearch import search
from pyrightarte import util as u
import requests
import os, sys
import time


def is_url_taken(url):
    try:
        response = requests.get(url)
        # Check if the response status code indicates success (e.g., 2xx)
        return response.status_code // 100 == 2
    except requests.RequestException:
        # An exception occurred, indicating that the URL is not reachable
        return False

def search_google(query, nr=1):
    final_res = False
    try:
        # Using the search function from the googlesearch library
        results = search(
                query, 
                num_results=nr, 
                timeout=2,
                sleep_interval=2)
        
        print("\n\nSearching google...\n")

        # Print the top 10 results
        
        def search_loop():
            try:
                fres = False
                for i, result in enumerate(results, start=0):
                    if final_res: 
                        break

                    res = u.extract_domain(result)
                    compare_res = u.compare_strings(query, res, 35)
                    if (res.__contains__("wikipedia")):
                        compare_res = False
                    
                    print(f"{i + 1}. {res} {u.compare_strings(query, res)}")

                    fres = compare_res
                return fres
            except Exception as e:
                print(e)

        
        final_res = u.execute_task_with_timeout(search_loop)
    
        print(query, final_res)
        if (final_res != None and final_res == True):
            return True
        time.sleep(2)
        url = f"https://www.{u.clean_and_lower(query)}.com"

        print(f"\n\nSearching direct url: www.{u.clean_and_lower(query)}.com\n")
    
        time.sleep(2)
        is_taken = u.is_url_taken(url)

        if (is_taken):
            final_res = True
        else:
            print("Url available")
            final_res = False

        return final_res

    
    except Exception as e:
        print(f"An error occurred: {e}")

def checkTaken(query: str):

    # You can customize the number of results if needed
    num_results_to_display = 3
    
    # Perform the search and display the results
    res = search_google(query, num_results_to_display)

    with open("output.txt", "a", encoding="utf8") as write_file:
        output = ""
        if (res):
            output = f"~~{query}~~"
        else:
            output = f"**{query}**"
        output += "\n"
        write_file.write(output)

if __name__ == "__main__":
    passwrd = input("password: ")
    if passwrd != "YXJ0ZWdsYWl2ZTIzMjR6":
        raise Exception("Wrong credentials!")

    with open("output.txt", "w", encoding="utf8") as write_file:
        write_file.write("")

    with open("input.txt", "a", encoding="utf8") as input:
        input.write("\n--END--")

    with open("input.txt", "r", encoding="utf8") as input_file:
        content = input_file.read().split("\n")
        for index, query in enumerate(content):
            if (query == "--END--"):
                sys.exit()
            
            os.system("cls")
            print(f"{index}/{len(content)-1}: {query}")
            print("["+f"="*(int(index/(len(content) - 1)*15))+f" "*(15-int(index/(len(content) - 1)*15))+"]")
            
            checkTaken(query)
