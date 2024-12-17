""" MAIN """

import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from apps.place_app import PlaceApp
from environment import Environment

load_dotenv()


def main() -> None:
    """ RUN """

    result = Environment(["API_KEY", "ACCESS_TOKEN", "PHONE_NUMBER_ID", "RECIPIENT_PHONE_NUMBER"]).verify()
    print(result)

    API_KEY = os.getenv("API_KEY")
    QUERIES = ["inşaat", "mühendislik", "emlak", "mimarlık", "yapı denetim", "nalbur", "müteahhit", "tekstil", "kuyumcu", "dernek", 
               "kentsel dönüşüm", "holding", "konut", "residence", "şirket"]
    OUTPUT_DIR = "query_results"

    parser = argparse.ArgumentParser(description="Main entry point for the project")

    parser.add_argument("--apps", type=str, nargs='+', required=True, choices=['app1', 'app2', 'app3'], help="The apps to run simultaneously")

    args = parser.parse_args()

    with ThreadPoolExecutor() as executor:
        futures = []
        if "app1" in args.apps:
            app1 = PlaceApp(API_KEY, QUERIES, OUTPUT_DIR)
            futures.append(executor.submit(app1.run))

        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
