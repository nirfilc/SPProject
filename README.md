# SPProject
## This is a geographic-based password meter based on [PESrank](https://github.com/lirondavid/PESrank/tree/master/PESrank)
## Prerequsits for local run:
### Server Side
* Clone the repository to your machine.
* Run `pip install -r requirements.txt`
* Download the model's text files from the university's nova server: nova.cs.tau.ac.il from the following path: `/specific/a/home/cc/students/csguests/nirfilc/SPProjectData`
* Unzip `GeneralDistribution` and `distributions` into the directory of the empty `modelData` directory in the repo on your machine. The structure should:
* - ./modelData
    - a1.txt
    - a2.txt
    - a3.txt
    - a4.txt
    - a5.txt
    - ./distributions
      - countries' directories    
* Run `app.py`
* Now the serever is listening. Deafult ip and port are localhost:5000.

### Client Side
To make a call to the password meter, ..... to be added


