# MIDI to Image conversion

The original repository can be found [here](https://github.com/mathigatti/midi2img).

- ## What does this fork do?

  I created this repository as a way to mine data samples for a future machine learning project of mine. 

  I manually downloaded about 2k songs in ``midi`` format and I wanted to adjust their format to something more interpretable by a neural network

- ## How is this accomplished?
  The obvious part is that I want images instead of audio/binary files as I believe those will be easier to work with. 

  The main new features found in this fork are the following:

  - All midi files that do not include piano instructions are filtered out
  - The images that are nearly empty are also filtered out as they would be bad training data (the *nearly empty* part is decided by counting how many vertical lines intersect no points in each image. I settled for a threshold of 18 as in, if there are more than 18 vertical lines with no intersections, the image gets discarded)
  - The elephant in the room; The file structure
    - You can no longer run ``img2midi`` or ``midi2img`` directly (although the code that allows you to do that is left in the files commented out). Instead you run ``main`` which uses both for you.
    - ``Data``: holds all the manually collected data. This is not used by the script but I am including this as well in case someone wants to use it.
    - ``midiFiles``: holds all the midi files that are in data and can produce images
    - ``midiOut``: this was used for debugging (using ``img2midi`` directly)
    - ``imgOut``: all outputted images are placed here
    - ``midiFinal``: ``imgOut`` contents mapped back to midi format

- ## What happens during execution?
  - The 2 output directories (namely ``midiOut``, ``midiFinal`` and ``imgOut``) are cleared
  - All midi files from ``midiFiles`` are split, filtered and converted to images which end up at ``imgOut``
  - All images in ``imgOut`` are converted back to midi files for potential future use and placed at ``midiFinal``
  - Finally, any file in ``midiFiles`` that got filtered out and did not make it to ``imgOut`` gets removed to save space and time for the next execution