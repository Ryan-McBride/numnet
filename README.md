# numnet
A script that turns a phrase into a [one-time pad](https://en.wikipedia.org/wiki/One-time_pad) and series of numbers. It also creates and uploads to vocaroo an audio file reading the series of numbers, to replicate the sound of a [numbers station.](https://youtu.be/BSxOjXC20Xo?t=19)

## OSX Installation

1. Install Homebrew
2. Clone this repository
3. `brew install ffmpeg`

## To Run

`python numnet.py <message> <one time pad (optional)>`

The one time pad is the encoded message. It will generate a random OTP if one is not provided.

The script will output the OTP, then the partnered number key. Incrementing the OTP's by the numbers will decode the message.

The numbers station audio is saved to a temp file and then uploaded to vocaroo so it can be distributed. Once the upload is compete the script will return the JSON from the vocaroo post, containing the url to share, and the delete token.

## Contribution Guidelines

I'll merge any contribution that adds better functionality, security, or is sufficiently cool.

## Other

You can use this code for whatever you want, I just wrote it because I was bored and numbers stations are cool.

Use Github issues for any feature requests or bug reports.
