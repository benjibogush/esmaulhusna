

git clone <repo>
cd <repo>
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt


📌 Additional Notes:

reportlab → PDF generation.

arabic-reshaper + python-bidi → Arabic text rendering.

pyinstaller → packaging into .dmg / .exe.

Add logging, argparse, json (but these are built-in, so no need in requirements.txt).


## Best Practice:
After every code change, run:
pip freeze > requirements.txt


## Old Readme steps below: used this for mac

Install necessary tools


pip install reportlab arabic-reshaper python-bidi

or 

python3 -m pip install reportlab arabic-reshaper python-bidi

or

python3 -m venv venv
source venv/bin/activate
pip install reportlab arabic-reshaper python-bidi

Then RUN App.py3

python3 ./app.py3

This file should be created in the same directory 
Esma_ul_Husna_99_Names_Of_Allah.pdf


use this cmd to exit venv
deactivate
