# A script to automatically fill inquiries from Postal Savings Bank (Serbia) and product a PDF that is ready to send back via email. 

These inquiries come every time a transfer arrives to your account from abroad. 
Filling them out each time is tedious and annoying, hence the nature of this script.

This script takes in a path to the PDF that has been sent to you as an argument and outputs a file that is ready to send in the same directory. 

## Usage

1. Clone the repository via `git clone https://github.com/Nek-12/AutoFillPostanska.git`
2. Install Python 3.12 or later (may work on earlier versions though)
3. Install dependencies using virtual env or simply `pip install -r requirements.txt`
4. Make a PNG file of your signature with transparency and place it in the folder as `signature.png` (or modify the script to set up the path manually)
5. Open `main.py` and modify the fields at the top, you are mainly looking for your ["money source" code](https://porezionline.rs/obrasci.php?pID=30209) and the regex to parse the invoice out of transaction number. If the invoice number is not found, the script will ask you for the number.
6. Now use `python3 main.py '<PathToFileFromEmail>` or start the script with `python3 main.py` and then drag the file into the terminal window.
7. Grab your file at the path that has been printed.
