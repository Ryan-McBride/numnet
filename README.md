[![Stories in Ready](https://badge.waffle.io/Ryan-McBride/numnet.png?label=ready&title=Ready)](https://waffle.io/Ryan-McBride/numnet)
# numnet
A script that turns a phrase into a [one-time pad](https://en.wikipedia.org/wiki/One-time_pad) and series of numbers. It also creates and uploads to vocaroo an audio file reading the series of numbers, to replicate the sound of a [numbers station.](https://youtu.be/BSxOjXC20Xo?t=19)

## OSX Installation

1. Install Homebrew
2. Clone this repository
3. `brew install ffmpeg`

## To Run

`$ python numnet.py <message> <-flags (optional)>`

The one time pad is the encoded message. It will generate a random OTP if one is not provided.

The script will output the OTP, then the partnered number key. Incrementing the OTP's by the numbers will decode the message.

The numbers station audio is saved to a temp file and then uploaded to vocaroo so it can be distributed. Once the upload is compete the script will return the JSON from the vocaroo post, containing the url to share, and the delete token.

Note: Vocaroo deletes uploaded audio after a few months.

## Command Flags

--pad Specify custom one-time pad

`$ python numnet.py "hello" --pad "UUFSE"`

--voice Specify an OSX say voice

`$ python numnet.py "imdabes" --voice "Agnes"`

a list of available voices can be seen by running `$ say -v '?'`

--chime Specify a custom chime to use. If not provided, a random built in chime will be used.

`$ python numnet.py "pizza time" --chime "./totinos.mp3"`

--output Specify a destination for the output file. If not used, a temp file will be created and uploaded to vocaroo (feels more like a broadcast that way)

`$ python numnet.py "remember trix yogurt?" --output "myBroadcast.mp3"`


## Contribution Guidelines

I'll merge any contribution that adds better functionality, security, or is sufficiently cool.

## Other

You can use this code for whatever you want, I just wrote it because I was bored and numbers stations are cool.

Use Github issues for any feature requests or bug reports.
