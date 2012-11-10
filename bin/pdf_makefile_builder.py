#!/usr/bin/python

import sys
from makefile_builder import MakefileBuilder

pdfs_to_build = [
#    (root-name, tag)
    ('MongoDB', 'Manual'),
    ('MongoDB-reference', 'manual'),
    ('MongoDB-use-cases', 'guide'),
]

def makefile_builder(name, tag):
    name_tagged = name + '-' + tag

    content = MakefileBuilder()

    content.target_break(name)
    content.target('$(branch-output)/latex/' + name + '.tex:latex')
    content.job('@sed $(SED_ARGS_FILE) -e $(LATEX_CORRECTION) -e $(LATEX_CORRECTION) -e $(LATEX_LINK_CORRECTION) $@')
    content.job('@echo [latex]: fixing $@ TeX from the Sphinx output.')

    content.target('$(branch-output)/latex/' + name_tagged + '.tex:$(branch-output)/latex/' + name + '.tex')
    content.job('@$(PYTHONBIN) bin/copy-if-needed.py -i $< -o $@ -b pdf')

    content.target('$(public-branch-output)/' + name_tagged + '-$(current-branch).pdf:$(branch-output)/latex/' + name_tagged + '.pdf')
    content.job('@cp $< $@')
    content.job('@echo [build]: migrated $@')

    content.target('$(public-branch-output)/' + name_tagged + '.pdf:$(public-branch-output)/' + name_tagged + '-$(current-branch).pdf')
    content.job('@bin/create-link $(notdir $<) $(notdir $@) $@')

    return content.makefile

def makefile_interactors(pdfs):
    output = ['.PHONY: manual-pdfs', '\n', 'manual-pdfs:$(PDF_OUTPUT)']

    for pdf in pdfs:
        output.append('\nPDF_OUTPUT += $(public-branch-output)/' + pdf[0] + '-' + pdf[1] + '.pdf')

    return output

class MongoDBManualPdfMakefile(object):
    def __init__(self):
        self.output = makefile_interactors(pdfs_to_build)
        for pdfs in pdfs_to_build:
            for item in makefile_builder(pdfs[0], pdfs[1]):
                self.output.append(item)

    def print(self):
        for line in self.output:
            print(line)

    def write(self, filename):
        with open(filename, 'w') as f:
            for line in self.output:
                f.write(line)

        print('[meta-build]: built "' + sys.argv[1] + '" to specify pdf builders.' )

def main():
    output = []

    makefile = MongoDBManualPdfMakefile()
    makefile.write(sys.argv[1])

if __name__ == '__main__':
    main()
