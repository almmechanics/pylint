# Copyright (c) 2018 Martin Palmer <martin.palmer@almmechanics.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Text formatting drivers for ureports"""

from __future__ import print_function

from pylint.reporters.ureports import BaseWriter


class MarkdownWriter(BaseWriter):
    """format layouts as text
    (ReStructured inspiration but not totally handled yet)
    """

    def begin_format(self):
        super(MarkdownWriter, self).begin_format()
        self.list_level = 0

    def visit_section(self, layout):
        """display a section as text
        """
        self.section += 1
        self.write('{} '.format('#'*self.section))
        self.format_children(layout)
        self.section -= 1
        self.writeln()

    def visit_evaluationsection(self, layout):
        """Display an evaluation section as a text."""
        self.section += 1
        self.format_children(layout)
        self.writeln()
        self.section -= 1
        self.writeln()

    def visit_title(self, layout):
        title = "# ".join(list(self.compute_content(layout)))
        self.writeln(title)


    def visit_paragraph(self, layout):
        """enter a paragraph"""
        self.format_children(layout)
        self.writeln()

    def visit_table(self, layout):
        """display a table as text"""
        
        table_content = self.get_table_content(layout)
        self.markdown_table(layout, table_content)
        self.writeln()

    def markdown_table(self, layout, table_content):
        row_zero = table_content[0]
        cols = len(row_zero)
        if layout.rheaders:
            # header
            self.write('|')
            for col in row_zero:
                self.write(('{}|').format(col.strip()))
            self.writeln('')

            # table spacers
            self.writeln('|{}'.format("-|"*cols))

            # body 
            for index, line in enumerate(table_content):
                if index != 0 :
                    self.write('|')
                    for col in line:
                        self.write(('{}|').format(col.strip()))
            
        else:

            # header
            self.writeln('|{}|'.format(" |"*cols))

            #table spacers
            self.writeln('|{}|'.format("-|"*cols))
            for index, line in enumerate(table_content):
                self.write('|')
                for col in line:
                    self.write(('{}|').format(col.strip()))
         

    def visit_verbatimtext(self, layout):
        """display a verbatim layout as text (so difficult ;)
        """

        for line in layout.data.splitlines():
            self.writeln("    {}".format(line))
        self.writeln()

    def visit_text(self, layout):
        """add some text"""
        if (layout.data.startswith('---')):
            self.writeln('---')
        else:
            self.writeln(layout.data)
