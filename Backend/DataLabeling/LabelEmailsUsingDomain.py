import tldextract
from world.database import Database # Source: https://gitlab.com/warsaw/world
from collections import defaultdict # Source: https://github.com/john-kurkowski/tldextract
import json

def create_origin_label(path):
    """
        Gets a path to a file containg rows of 'email:password' pairs and returns an array of json of the following format:
        {{\n
            email: "email",\n
            password: "password"\n
            country: "country"\n
        }}

    """
    json_array = []
    file = open(path, 'rb')
    emailPasswordPairs = file.readlines()
    db = Database()
    domains_count = defaultdict(int)
    for emailPasswordPair in emailPasswordPairs:
        string_content = emailPasswordPair.decode('unicode_escape')
        try:
            [email, password] = parse_email_password(string_content)
        except:
            continue
        tld = parse_domain(email)
        country = db.lookup_code(tld)
        curr_json = {
            "email": email,
            "password": password,
            "country": country
        }
        json_array.append(json.dumps(curr_json))
        domains_count[country] += 1
    return json_array
    

def parse_email_password(str):
    """
        Gets an "email:password" or "email;password" string and returns an array of [email, password].
        If can't split string on ':'/';', return null
    """
    try:
        [email, password] = str.split(":", 1)
    except:
        try:
            [email, password] = str.split(";", 1)
        except:
            return
    return [email, password]

def parse_domain(email):
    """
        Gets an email address and returns its tld (top-level domain), e.g name@email.co.il => il
    """
    extract_result = tldextract.extract(email)
    suffix = extract_result.suffix 
    tld = suffix.split(".")[-1]
    return tld

path = "C:/Users/nirfi/Downloads/BreachCompilation/data/i/u"

create_origin_label(path)