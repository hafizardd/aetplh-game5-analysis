""""LiveChatScraper class, used to scrape live chat data from a youtube stream."""
import time
from math import floor
from typing import Optional

from livechat_scraper.constants import node_constants as nc
from livechat_scraper.constants import scraper_constants as con
from livechat_scraper.builders.player_state import PlayerState
from livechat_scraper.generators.output_generator import OutputGenerator
from livechat_scraper.requestors.subsequent_requestor import SubsequentRequestor
from livechat_scraper.scrapers.scraper_initializer import ScraperInitializer
from livechat_scraper.scrapers.video import Video
from livechat_scraper.builders.message_factory import messageFactory

CONTINUATION_FETCH_BASE_URL = "https://www.youtube.com/youtubei/v1/next?"


def parse_time_to_ms(time_str: str) -> int:
    """Convert time string in 'HH:MM:SS', 'H:MM:SS', 'MM:SS', or 'M:SS' format to milliseconds.
    
    Args:
        time_str: Time string like '1:30:00' (1 hour 30 min), '5:30' (5 min 30 sec),
                  or '5:05:22' (5 hours 5 min 22 sec)
    
    Returns:
        Time in milliseconds
    
    Raises:
        ValueError: If the time string format is invalid
    """
    if not time_str:
        raise ValueError("Time string cannot be empty")
    
    parts = time_str.strip().split(':')
    
    if len(parts) == 2:
        # MM:SS format
        minutes, seconds = int(parts[0]), int(parts[1])
        hours = 0
    elif len(parts) == 3:
        # HH:MM:SS format
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
    else:
        raise ValueError(f"Invalid time format: '{time_str}'. Expected 'HH:MM:SS' or 'MM:SS'")
    
    if seconds < 0 or seconds >= 60:
        raise ValueError(f"Seconds must be between 0 and 59, got {seconds}")
    if minutes < 0 or minutes >= 60:
        raise ValueError(f"Minutes must be between 0 and 59, got {minutes}")
    if hours < 0:
        raise ValueError(f"Hours cannot be negative, got {hours}")
    
    total_ms = ((hours * 3600) + (minutes * 60) + seconds) * 1000
    return total_ms

class LiveChatScraper:
    """"entry point for live chat scraper, this is exposed object 
    that someone would use to scrape livechat contents"""
    output_filename = 'outputContent.json'
    invalid_characters = "<>:\"/\\|?*"
    sleepValue = 3

    def __init__(self, video_url: str, start_time: Optional[str] = None, 
                 end_time: Optional[str] = None, debug_mode: bool = False):
        """Initialize the LiveChatScraper.
        
        Args:
            video_url: The YouTube video URL to scrape live chat from.
            start_time: Optional start time in 'HH:MM:SS' or 'MM:SS' format.
                       If None, starts from the beginning of the video.
                       Example: '1:30:00' for 1 hour 30 minutes.
            end_time: Optional end time in 'HH:MM:SS' or 'MM:SS' format.
                     If None, scrapes until the end of the video.
                     Example: '2:00:00' for 2 hours.
            debug_mode: Enable debug mode for additional output.
        """
        self.video = Video(None, video_url, None)
        self.is_debugging = debug_mode
        self.content_set = []
        self.__extract_video_id()
        self.player_state = PlayerState()
        self.video_end_time = 0  # Full video duration in ms
        self.user_start_time_ms = 0  # User-specified start time in ms
        self.user_end_time_ms = 0  # User-specified end time in ms (0 = use video end)
        self.initialization_successful = False
        self.requestor = None
        
        # Parse user-specified time range
        if start_time is not None:
            self.user_start_time_ms = parse_time_to_ms(start_time)
        if end_time is not None:
            self.user_end_time_ms = parse_time_to_ms(end_time)
        
    def __set_initial_parameters(self):
        try:

            self.player_state.continuation = ScraperInitializer()\
                .generate_initial_state(self.video.video_id)
            initial_content = ScraperInitializer().generate_initial_content(self.video.video_url)
            self.video.video_title = self.__clean_filename(initial_content["videoDetails"]["title"])
            self.output_filename = f'{self.video.video_title}_{time.time()}'
            self.video_end_time = int(initial_content["streamingData"]["formats"][0]["approxDurationMs"])
            
            # Set scraping end time: use user-specified end time or full video duration
            if self.user_end_time_ms > 0:
                # Validate user end time doesn't exceed video length
                if self.user_end_time_ms > self.video_end_time:
                    print(f"Warning: Specified end time exceeds video duration. "
                          f"Using video end time instead.")
                    self.user_end_time_ms = self.video_end_time
            else:
                self.user_end_time_ms = self.video_end_time
            
            # Validate start time
            if self.user_start_time_ms >= self.user_end_time_ms:
                raise ValueError(f"Start time ({self.user_start_time_ms}ms) must be less than "
                               f"end time ({self.user_end_time_ms}ms)")
            
            # Set initial player offset to user start time for efficient scraping
            self.player_state.player_offset_ms = self.user_start_time_ms
            
            self.initialization_successful = True
        except Exception as e:
            print(f"error encountered attempting to set initial parameters: {e}")

    def __extract_video_id(self):
        key_start = self.video.video_url.find('watch')+8
        if key_start <= 8:
            key_start = self.video.video_url.find("live/")+5
        key_end = key_start + self.video.VIDEO_ID_LENGTH
        self.video.video_id = self.video.video_url[key_start:key_end]

    def __clean_filename(self, output_filename):
        for char in self.invalid_characters:
            output_filename = output_filename.replace(char, '')
        return output_filename

    def __parse_subsequent_contents(self):
        self.requestor.make_request()
        try:
            action_contents = self.requestor.response["continuationContents"]\
                ["liveChatContinuation"]["actions"][1::]
            for content in action_contents:
                replay_action = content["replayChatItemAction"]
                # Filter messages based on user-specified time range
                offset_ms = int(replay_action.get("videoOffsetTimeMsec", 0))
                
                # Skip messages before the start time
                if offset_ms < self.user_start_time_ms:
                    continue
                
                # Stop adding messages after end time (but continue to update offset)
                if offset_ms > self.user_end_time_ms:
                    continue
                
                self.content_set.append(replay_action)
            self.player_state.continuation = self.requestor.update_continuation\
                (self.requestor.response)
            self.player_state.player_offset_ms = self.__find_final_offset_time_from_response(
                action_contents)
            self.requestor.update_fetcher\
                (self.player_state.continuation, self.player_state.player_offset_ms)
        except KeyError:
            print(self.requestor.response)
            self.player_state.continuation = con.SCRAPE_FINISHED

    def __find_final_offset_time(self):
        final_content = self.content_set[-1]
        return final_content["videoOffsetTimeMsec"]

    def __find_final_offset_time_from_response(self, action_contents):
        """Find the final offset time from the raw response actions.
        
        This is used instead of __find_final_offset_time because content_set
        may not include all messages due to time filtering.
        """
        if action_contents:
            final_action = action_contents[-1]
            return final_action["replayChatItemAction"].get("videoOffsetTimeMsec", 0)
        return self.player_state.player_offset_ms

    def scrape(self):
        """Method to call scrape functionality and pull livechat data.
        
        Scrapes live chat messages within the specified time range.
        If start_time was specified, only messages from that time onward are collected.
        If end_time was specified, scraping stops when that time is reached.
        """
        self.__set_initial_parameters()
        if not self.initialization_successful:
            print("Unable to initialize scraper successfully, quitting")
            return False
        self.requestor = SubsequentRequestor(self.video.video_id, self.player_state)
        self.requestor.build_fetcher()
        
        # Display time range information
        start_str = self.__ms_to_time_string(self.user_start_time_ms)
        end_str = self.__ms_to_time_string(self.user_end_time_ms)
        print(f'Beginning livechat scraping from {start_str} to {end_str}')
        
        self.__parse_subsequent_contents()
        has_slept = True
        current_interval = 0
        
        # Calculate total scrape range for accurate progress display
        scrape_range = self.user_end_time_ms - self.user_start_time_ms
        
        while(int(self.player_state.player_offset_ms) < self.user_end_time_ms \
            and self.player_state.continuation != con.SCRAPE_FINISHED):
            try:
                # Calculate progress within the specified range
                elapsed = int(self.player_state.player_offset_ms) - self.user_start_time_ms
                progress = float(elapsed) / float(scrape_range) if scrape_range > 0 else 1.0
                progress = min(max(progress, 0.0), 1.0)  # Clamp between 0 and 1
                
                current_time_str = self.__ms_to_time_string(int(self.player_state.player_offset_ms))
                print(f'progress: {progress:.2%} (at {current_time_str})', end="\r")
                
                floored_progress = floor(progress * 100)
                if current_interval != floored_progress:
                    has_slept = False
                if(floored_progress % 10 == 0 and not has_slept):
                    time.sleep(self.sleepValue)
                    current_interval = floored_progress
                    has_slept = True
                self.__parse_subsequent_contents()
            except Exception as ex:
                print("scraping failed")
                print(f"Exception encountered: {str(ex)}")
        print(f"\nscraping completed - collected {len(self.content_set)} messages")
        return True

    def __ms_to_time_string(self, ms: int) -> str:
        """Convert milliseconds to HH:MM:SS format string."""
        total_seconds = ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    def output_messages(self):
        """"build a messages list that contains all the chat messages"""
        messages = []
        builder = messageFactory()

        for content in self.content_set:
            payload = content[nc.ACTIONS_NODE][0]
            if nc.TICKER_ITEM_ACTION_NODE in payload:
                pass
            else:
                message = builder.build(payload)
                message.build_message()
                messages.append(message.generate_content())
        return messages

    def write_to_file(self, write_type, output_filename = None, output_path = None):
        """"writes currently scraped content to a file output"""
        if output_filename is None:
            output_filename = f'{write_type}_{self.output_filename}'
        generator = OutputGenerator(output_filename, output_path)
        if write_type != con.OUTPUT_RAW:
            generator.generate(self.output_messages(), write_type)
        else:
            generator.generate(self.content_set, write_type)
