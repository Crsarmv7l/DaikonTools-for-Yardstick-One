# DaikonTools-for-Yardstick-One

What is it?

This are tools for the Yardstick One Radio dongle to receive/save/send RF signals via a .ys1 file. It allows users to easily receive, save, send or create a saved signal by hand and transmit it without having to use the Rfcat interactive shell, or write their own python scripts.
  
The .ys1 file format:

RX saves signals in the correct format if desired. Hand editing is easy, analyze in URH, then create a .ys1 through any text editor.  The DaikonTX script run, the file name typed in and the signal sent according to the parameters in the .ys1 file.
  
  Required entries:
 - If you save a recieved signal via DaikonRX all of the below will be done for you, simply enter a filename.
  
- Entries must be in the order set forth in the ASK/FSK examples
- Frequency must be entered to two decimals eg 315.00 or 433.92
- Modulation must be either ASK or FSK
- Baud rate must be entered
- Deviation must be entered for FSK 
- If repeats are set to 0 replay will be continuous
- Preamble is Optional
- Data should be entered in hex
  
Features:

  - Multiple saves are possible while RXing
  - RX/TX tools for the format with flipper .subs support in progress
  - Easily editable
  - ASK/FSK modulations
  - Continuous transmission
  - File format is a text representation of the signal, so size is small
  - Error checks hex data for length before converting to bytes
  - Rapid and easy method for sending signals, create or save a .ys1 and send it.
  - Amp setting is included in the python script but will need to be uncommented.
  
Why?

I created this due to the lack of decent Yardstick One tools, which is a shame given how awesome the device is. RFCrack is pretty decent but does not save things like freq which can make it a pain to send a saved signal, and doesn't set the dongle back to idle which is a necessity. I was also inspired by the Flipper Zero .sub file format which is very similar.

Usage:

Download the python script, change the location in def main() where your .ys1 files will be located eg: home = os.path.expanduser( '~/Saved_TX/' ). This same line is also in DaikonRX and may need to be changed for you. Create/receive and save .ys1 files, then rn DaikonTX and Send.

# In Progress:
- Flipper RAW Format
- ~~RX that allows saving to my format~~
  - RX resending
    - RX save after resending
- Expanding this to include the above

Like all my stuff I work on it as I feel like it/have time. I don't put up partial code, only things that I know work. 

# License:

This software is provided without warranty or liability on the part of the author. It is free of charge and may be forked, modified, and utilized for all non-commercial and non-retail applications provided attribution is given, this license is included and source code is disclosed. Commercial use of this software is strictly prohibited. I welcome pull requests.

Yardstick One is a product/trademark of Great Scott Gadets.
