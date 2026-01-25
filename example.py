""""example to see how the live chat scraper scrapes and outputs data."""
import sys
import time
from livechat_scraper.scrapers import livechat_scraper
from livechat_scraper.constants import scraper_constants as sCons


def test_scraper_output(video_url, start_time=None, end_time=None):
    """"livechat scraper example, scrapes a video URL and outputs the content 
        to a JSON, txt, and raw file.
        
    Args:
        video_url: The YouTube video URL to scrape.
        start_time: Optional start time in 'HH:MM:SS' or 'MM:SS' format.
                   Example: '1:30:00' for 1 hour 30 minutes.
        end_time: Optional end time in 'HH:MM:SS' or 'MM:SS' format.
                 Example: '2:00:00' for 2 hours.
    """
    start_run_time = time.time()
    scraper = livechat_scraper.LiveChatScraper(
        video_url, 
        start_time=start_time, 
        end_time=end_time
    )
    scraper.scrape()
    # saves all messages in a file as a json object
    scraper.write_to_file(sCons.OUTPUT_JSON, "testJson_"+scraper.output_filename)
    # saves all messages in a txt file, each line is a message entry
    scraper.write_to_file(sCons.OUTPUT_TEXT, "testText_"+scraper.output_filename)
    # saves all messages in a json file preserving the raw json that comes over when making the request call to youtube
    scraper.write_to_file(sCons.OUTPUT_RAW, "testRaw_"+scraper.output_filename)
    end_run_time = time.time()
    print(f'program runtime: {end_run_time - start_run_time}')


def test_scraper_with_time_range():
    """Example: Scrape only a specific time range of a live video.
    
    This example shows how to scrape comments from minutes 90 to 120
    of a 2-hour live video (i.e., from 1:30:00 to 2:00:00).
    """
    video_url = "https://www.youtube.com/watch?v=MNraBP_LoNM"
    
    # Scrape from 1 hour 30 minutes to 2 hours
    scraper = livechat_scraper.LiveChatScraper(
        video_url,
        start_time="1:30:00",  # Start at 90 minutes (1 hour 30 min)
        end_time="2:00:00"     # End at 120 minutes (2 hours)
    )
    scraper.scrape()
    scraper.write_to_file(sCons.OUTPUT_JSON, "timeRange_"+scraper.output_filename)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Default: scrape full video
        test_scraper_output("https://www.youtube.com/watch?v=MNraBP_LoNM")
    elif len(sys.argv) == 2:
        # Single argument: video URL, scrape full video
        test_scraper_output(sys.argv[1])
    elif len(sys.argv) == 4:
        # Three arguments: video URL, start_time, end_time
        # Example: python example.py https://youtube.com/watch?v=VIDEO_ID 1:30:00 2:00:00
        test_scraper_output(sys.argv[1], start_time=sys.argv[2], end_time=sys.argv[3])
    else:
        print("Usage:")
        print("  python example.py                              # Scrape default video")
        print("  python example.py <video_url>                  # Scrape full video")
        print("  python example.py <video_url> <start> <end>    # Scrape time range")
        print("")
        print("Time format: HH:MM:SS or MM:SS")
        print("Example: python example.py https://youtube.com/watch?v=XXX 1:30:00 2:00:00")
