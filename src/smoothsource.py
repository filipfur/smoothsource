import template.template
import sys
import os
import getopt

class smoothsource:

    template = template.template

    templates = {}

    def createTemplate(templatepath):
        tmpl = None
        if templatepath in smoothsource.templates:
            tmpl = smoothsource.templates[templatepath]
        else:
            tmpl = template.template.Template(templatepath)
            smoothsource.templates[templatepath] = tmpl
        return tmpl

    def populateTemplate(templatepath, parameters):
        tmpl = smoothsource.createTemplate(templatepath)
        tmpl.generate(parameters)


def main():
    opts, args = getopt.getopt(sys.argv[1:], "vt:p:", ["version", "template=", "payload="])
    print(opts)
    #smoothsource

if __name__ == "__main__":
    main()