from smoothsource import smoothsource

def main():

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

if __name__ == "__main__":
    main()