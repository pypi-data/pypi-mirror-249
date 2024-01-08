import re
from re import Pattern

from ormspace.bases import AbstractRegex


class Package(AbstractRegex):
    GROUP_PATTERN = re.compile(r'(?P<size>\d+[.,]\d+|\d+)(\s+)?(?P<content>[\w\-]+(\s[\w\-]+)+|[\w\-]+)')


class ActiveDrug(AbstractRegex):
    GROUP_PATTERN = re.compile(r'(?P<name>[\w\-]+(\s[\w\-]+)+|[\w\-]+)\s+(?P<strength>\d+[.,]\d+|\d+)\s?(?P<unit>\w+/\w+|\w+)')


class ProfessionalId(AbstractRegex):
    GROUP_PATTERN = re.compile(r'(?P<ref1>\w+)\s(?P<ref2>[\w\-]+)|(?P<ref3>\w+)')
    


if __name__ == '__main__':
    x = ProfessionalId('CRM 9553GO')
    print(x.groupdict())
    print(x)
