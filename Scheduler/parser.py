import yaml
from yaml.loader import FullLoader


# with open('schedule.yml') as fd:

#     d = yaml.load_all(fd)
#     from pprint import pprint

#     for i in d:
#         pprint(i)

with open('Scheduler/schedule.yml') as fd:

    d = yaml.load(fd,Loader=FullLoader)
    from pprint import pprint

pprint(d)