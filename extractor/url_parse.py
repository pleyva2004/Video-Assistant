import re

# Regex to extract everything after watch?v=
pattern = r"watch\?v=(.+)"

def get_video_id(url):
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        raise ValueError(f"No video ID found in URL: {url}")

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=NpCx0qjHlBQ&t=27s"
    print(get_video_id(url))