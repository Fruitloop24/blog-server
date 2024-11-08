from fetch_newsletters import fetch_newsletters
from generate_synopsis import generate_individual_synopsis, generate_overall_synopsis
from generate_html import generate_combined_html, save_html_output, get_latest_three_blog_dates

def main():
    newsletters = fetch_newsletters()
    synopses = []
    if newsletters:
        for content in newsletters:
            synopsis = generate_individual_synopsis(content)
            if synopsis:
                synopses.append(synopsis)
                print(f"Generated individual synopsis:\n{synopsis}\n")
        if synopses:
            overall_synopsis = generate_overall_synopsis(synopses)
            if overall_synopsis:
                print(f"Generated overall synopsis:\n{overall_synopsis}\n")
                
                # Fetch the latest blog dates
                latest_blog_dates = get_latest_three_blog_dates()

                # Generate and save the HTML output
                html_output = generate_combined_html(overall_synopsis, latest_blog_dates)
                save_html_output(html_output)
            else:
                print("Failed to generate overall synopsis.")
        else:
            print("No individual synopses generated.")
    else:
        print("No newsletters to process.")

if __name__ == "__main__":
    main()
