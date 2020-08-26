class ButtonCategory:
    def __init__(self, buttonType):
        self.category = {}
        self.makeCategoryWithType(buttonType)

    def makeCategoryWithType(self, buttonType):
        self.category = {
            'type': buttonType,
            'names': [],
            'defaults': []
        }        
        
    def addButtons(self, names):
        self.category['names'] += names

    def addDefaults(self, names):
        self.category['defaults'] += names

    def __iadd__(self, other):
        other = other.asDict()
        self.addButtons(other['names'])
        self.addDefaults(other['defaults'])
        return self

    def asDict(self):
        return self.category
    

class Categories:
    def __init__(self):
        self.categories = {}
        
    def addCategory(self, name, category):
        self.categories[name] = category

    def __iter__(self):
        for name, category in self.categories.items():
            yield name, category
        
    def __iadd__(self, other):
        for name, category in other:
            if name in self.categories:
                self.categories[name] += category
            else:
                self.categories[name] = category

        return self

    def __getitem__(self, key):
        return self.categories[key]

    def asDict(self):
        return {name: category.asDict() for name, category in self.categories.items()}
