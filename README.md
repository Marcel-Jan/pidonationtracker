# Tour for Life donation tracker for the Raspberry Pi with e-ink display.
This is my Python code to display the gift amount I have gathered for Tour for Life 2025 on a Raspberry Pi Zero 2 with Inky Impressions 7.3 e-ink display.

I use this for our sponsoring events where we collect sponsoring for the Daniel den Hoed Foundation, for cancer research. The display shows the people who donate the updated gift amount. The code has been updated to scrape the gift amount from [my personal sponsor page of Tour for Life]([http://example.com](https://supporta.com/lfqd/z0qpn9xqox)). The Tour for Life page has been changed quite a lot since last year.

![Photo of the e-ink display with a donation amount and background image of cyclists](JPEG-afbeelding-4060-A766-84-0.jpeg?raw=true)


## Changing the sponsor link
In pydonationtracker2025_inky.py there's a variable called personal_url where I put the url of my Tour for Life 2025 sponsor page.

## Running the script
Copy the code to /home/youruser/PythonProjects/pidonationtracker.

Install pipx and poetry:
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    pipx install poetry

From the pidonationtracker directory:
Run poetry install:
    poetry install

Run poetry shell:
    poetry shell

    python3 src/pidonationtracker/pydonationtracker2025_inky.py

That should do it.
