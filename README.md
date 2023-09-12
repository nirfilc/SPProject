# SPProject
## This is a geographic-based password meter based on [PESrank](https://github.com/lirondavid/PESrank/tree/master/PESrank)
## Prerequsits for local run:
python 3
### Server Side
* Clone the repository to your machine.
* cd to it: `cd ./SPProject`
* Run `pip install -r requirements.txt`
* Download the model's text files from the university's nova server: nova.cs.tau.ac.il from the following path: `/specific/a/home/cc/students/csguests/nirfilc/SPProjectData`
* Unzip `GeneralDistribution` and `distributions` into a directory of your choise on your machine. The structure should be:
* - ./modelData
    - a1.txt
    - a2.txt
    - a3.txt
    - a4.txt
    - a5.txt
    - ./distributions
      - countries' directories
* Make sure the var `path` on line 9 in the file `app.py` is updated to where the models text files are saved (production path is different). 
* Run `python app.py`
* Now the serever is listening. Deafult ip and port are localhost:5000.

### Client Side
follow these instructions: [Frontend](https://github.com/naderkhalaila/Password-Strength-Checker-in-React-main-2#running-the-application-locally)


