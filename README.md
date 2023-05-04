# DaikonTX-for-Yardstick-One

What is it?

This is a tool for the Yardstick One Radio dongle to send RF signals that have been saved as a .ys1 file according to the given format. It allows users to easily create a saved signal and transmit it without having to use the Rfcat interactive shell, or write their own python scripts.
  
The .ys1 file format:

Is easily readable and editable through any text editor. Parameters are entered into the file, and saved. The DaikonTX script run, the file name typed in and the signal sent according to the parameters in the .ys1 file.
  
  Required entries:
  
- Entries must be in the order set forth in the ASK/FSK examples
- Frequency must be entered to two decimals eg 315.00 or 433.92
- Modulation must be either ASK or FSK
- Baud rate must be entered
- Deviation must be entered for FSK 
- If repeats are set to 0 replay will be continuous
- Preamble is Optional
- Data should be entered in hex
  
Features:

  - Multiple saves are possible, provided the formats are followed and they will be parsed and filenames displayed when running the script
  - Easily editable
  - ASK/FSK modulations
  - Continuous transmission
  - File format is basically a text representation of the signal, so size is small
  - Error checks hex data for length before converting to bytes
  - Rapid and easy method for sending signals, create a .ys1 and send it.
  - Amp setting is included in the python script but will need to be uncommented.
  
Why?

I created this due to the lack of decent Yardstick One tools, which is a shame given how awesome the device is. RFCrack is pretty decent but does not save things like freq which can make it a pain to send a saved signal, and doesn't set the dongle back to idle which is a necessity. I was also inspired by the Flipper Zero .sub file format which is very similar.

Usage:

Download the python script, change the location in def main() where your .ys1 files will be located eg: home = os.path.expanduser( '~/Saved_TX/' ). Create a (or many) .ys1 file, run the script, type in the name of the .ys1 you want to send from the list. Root access is not needed (and is detrimental) provided you don't need root access to access your Yardstick One.

# In Progress:
- Flipper RAW Format
- RX that allows saving to my format
- Expanding this to include the above

Like all my stuff I work on it as I feel like it/have time. I don't put up partial code, only things that I know work. 

# License:

This software is provided without warranty or liability on the part of the author. It is free of charge and may be forked, modified, and utilized for all non-commercial and non-retail applications provided attribution is given, this license is included and source code is disclosed. Commercial use of this software is strictly prohibited. I welcome pull requests.

Yardstick One is a product/trademark of Great Scott Gadets.
