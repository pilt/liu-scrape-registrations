Scrape Linköping University's student portal for course registrations. Uses 
[Requests](http://docs.python-requests.org/en/latest/index.html) and 
[pyquery](http://packages.python.org/pyquery/) for scraping.

## Dependencies

Run `pip install -r requirements.txt`.

## Example

    $ cat liu_ids.txt
    fooba000
    abcxy555
    $ ./scrape.py -u abcde123 liu_ids.txt
    Password: 
    no regs for fooba000
    dump saved in liu_ids.txt.p

    Summary:
        1  Multicore- och GPU-Programmering (TDDD56-HT2011)
        1  Processprogrammering och operativsystem (TDDB68-HT2011)
        1  Optimering av stora system (TAOP34-HT2011)
        1  Programmering och datastrukturer (TDDC76-HT2011)
        1  Datautvinning med matrismetoder (TANA07-HT2011)

Except for showing a summary, information is dumped in *liu_ids.txt.p* with some
additional information.
    
    $ python
    >>> import pickle
    >>> from pprint import pprint
    >>> dump = pickle.load(open('liu_ids.txt.p', 'rb'))
    >>> pprint(dump)
    {'course_names': {u'TANA07-HT2011': u'Datautvinning med matrismetoder',
                      u'TAOP34-HT2011': u'Optimering av stora system',
                      u'TDDB68-HT2011': u'Processprogrammering och operativsystem',
                      u'TDDC76-HT2011': u'Programmering och datastrukturer',
                      u'TDDD56-HT2011': u'Multicore- och GPU-Programmering'},
     'course_reg_counts': defaultdict(<type 'int'>, {u'TDDB68-HT2011': 1, ... }),
     'course_regs': defaultdict(<type 'list'>, {u'TDDB68-HT2011': ['abcxy555'], ... })}

