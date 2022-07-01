from smoothsource import smoothsource

def _default(*args):
    return shoppingList(*args)

def shoppingList():
    classtemplate = smoothsource.createTemplate("template/shoppinglist.smoothsource")
    content = classtemplate.generate(payload={
        "author": "Karl Alfred",
        "items": [
            {
                "item": "Eggs",
                "quantity": 12
            },
            {
                "item": "Milk",
                "quantity": 2
            },
            {
                "item": "Flour",
                "quantity": 1
            }
        ]
    })
    print(content)
    return True

def test(value):
    print("You wrote: " + str(value))
    return True