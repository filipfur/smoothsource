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
        return tmpl.generate(parameters)

    def generate(templatepath, parameters, outputFile=None, overwrite=False):
        if outputFile and not overwrite and os.path.exists(outputFile):
            print("File already exist, overwrite?")
            return False
        rval = True
        try:
            data = smoothsource.populateTemplate(templatepath, parameters) 
            if outputFile is None:
                print(data)
            else:
                with open(outputFile, 'w') as f:
                    f.write(data)
        except Exception as e:
            print(e)
            rval = False

        return rval


def main():
    #opts, args = getopt.getopt(sys.argv[1:], "vt:p:", ["version", "template=", "payload="])
    #print(opts)
    #templatepath = None
    #payload = None
    #for opt, arg in opts:
    #    if opt in ("-t", "--template="):
    #        templatepath = arg
    #    elif opt in ("-o", "--payload="):
    #        payload = arg
    #template = smoothsource.createTemplate(templatepath)
    #template.generate(payload=payload)

    # TODO: Flag -i to init directory with smoothfile.py template

    target = "_default"
    try:
        target = "_" + sys.argv[1]
    except:
        pass
    args = sys.argv[2:]
    rval = False
    try:
        import smoothfile
        func = getattr(smoothfile, target)
        rval = func(*args)
    except Exception as e:
        print(e)
    if rval:
        print("smooth: Finished sucesfully.")
    else:
        print("smooth: Execution failed.")




if __name__ == "__main__":
    main()