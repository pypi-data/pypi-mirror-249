import re
from re import Pattern

from ormspace.bases import AbstractRegex


class Package(AbstractRegex):
    
    @property
    def pattern(self) -> Pattern:
        return re.compile(r'(?P<size>\d+[.,]\d+|\d+)\s+(?P<content>[\w\-]+(\s[\w\-]+)+|[\w\-]+)')
    
    @property
    def resolve(self) -> str:
        return '{size} {content}'.format(**self.group_dict()).lower()



class ActiveDrug(AbstractRegex):
    
    def __init__(self, value):
        super().__init__(value)
        for k, v in self.groupdict().items():
            setattr(self, k, v)
    
    @property
    def pattern(self) -> Pattern:
        return re.compile(r'(?P<name>[\w\-]+(\s[\w\-]+)+|[\w\-]+)\s+(?P<strength>\d+[.,]\d+|\d+)\s?(?P<unit>\w+/\w+|\w+)')
    
    @property
    def resolve(self) -> str:
        data = self.groupdict()
        return '{name} {strength} {unit}'.format(**data).lower()


class ProfessionalId(AbstractRegex):
    @property
    def pattern(self) -> Pattern:
        return re.compile(r'(?P<regulator>\w+)\s(?P<id>[\w\-]+)')
    
    @property
    def resolve(self) -> str:
        data = self.group_dict()
        return '{regulator} {id}'.format(**data).lower()


# class ActiveDrug(AbstractRegex):
#
#     def __str__(self):
#         data = self.group_dict()
#         return f'{data.get("name").title()} {data.get("dose")} {data.get("unit").lower()}'
#
#     @property
#     def pattern(self) -> Pattern:
#         return re.compile(r'(?P<name>[\w\-]+(\s[\w\-]+)+|[\w\-]+)\s(?P<dose>\d+[.,]\d+|\d+)\s?(?P<unit>\w+/\w+|\w+)')
#


if __name__ == '__main__':
    x = ActiveDrug('25-hidroxi vitamina D 12,5mg/ml')
    print(x.group_dict())
    print(x)