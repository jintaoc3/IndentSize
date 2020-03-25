import sublime
import sublime_plugin

class IndentSizeCommand(sublime_plugin.TextCommand):
    def indent(self, edit, line, start):
        start_point = start.begin()

        tab_size = self.view.settings().get("tab_size")
        indent_size = self.view.settings().get("indent_size", tab_size)
        if indent_size > tab_size:
            indent_size = tab_size
		
        indentation_region = sublime.Region(line.begin(), start_point)
        indentation = self.view.substr(indentation_region)

        # Figure out the true length of the indentation (in spaces)
        indentation_length = indentation.replace(" " * tab_size, "\t")
        indentation_length = indentation_length.replace(" \t", "\t").replace("\t", " " * tab_size)
        indentation_length = len(indentation_length)
        #println(indentation_length)
        # How many trailing spaces are there in the indentation:
        trailing_spaces = len(indentation) - len(indentation.rstrip(" "))
        lastStop = indentation[indentation.rfind("\t")+1:]
        lastStop.replace(" ","");
        lastStop= len(lastStop)
        # How many characters are there from the last indent stop:
        indent_mod = lastStop % indent_size

        #indent_mod = 0
        # How many spaces are there from the last tab stop:
        lastStopS = indentation[indentation.rfind("\t")+1:].count(" ");
        trailing_tab = min(lastStopS, trailing_spaces) % tab_size

        #if tab_size == indent_size or trailing_tab + indent_size == tab_size:
        if tab_size == indent_size or start_point == line.begin():
            trailing = trailing_tab 
            tab = "\t"
        else:
            trailing = 0
            tab = " " * (indent_size - indent_mod)
        if start_point == line.begin():
            tab = "\t"
        #trailing = trailing_tab
        # Do actual indent
        if trailing:
            indentation_region = sublime.Region(start_point - trailing, start_point)
            self.view.erase(edit, indentation_region)
        self.view.insert(edit, start_point - trailing, tab)
        

    def run(self, edit):
        sel = self.view.sel()
        for region in reversed(sel):
            if region.empty():
                line = self.view.line(region)
                start = self.view.find("[^ \t]", line.begin())
                if start is None:
                    start = line
                #start = line
                self.indent(edit, line, start)
                if sel.contains(region):
                    sel.subtract(region)
                    region.a += 1
                    region.b += 1
                    sel.add(region)
            else:
                for line in reversed(self.view.lines(region)):
                    if line.a != line.b:
                        start = self.view.find("[^ \t]", line.begin())
                        #start = line
                        if start is None:
                            start = line
                        self.indent(edit, line, start)


class UnindentSizeCommand(sublime_plugin.TextCommand):
    def unindent(self, edit, line, start):
        start_point = start.begin()

        tab_size = self.view.settings().get("tab_size")
        indent_size = self.view.settings().get("indent_size", tab_size)
        if indent_size > tab_size:
            indent_size = tab_size

        indentation_region = sublime.Region(line.begin(), start_point)
        indentation = self.view.substr(indentation_region)

        # Figure out the true length of the indentation (in spaces)
        indentation_length = indentation.replace(" " * tab_size, "\t")
        indentation_length = indentation_length.replace(" \t", "\t").replace("\t", " " * tab_size)
        indentation_length = len(indentation_length)

        # How many characters are there from the last indent stop:
        # indent_mod = indentation_length % indent_size
        # if not indent_mod:
        #     indent_mod = indent_size
        lastStop = indentation[indentation.rfind("\t")+1:]
        lastStop = len(lastStop)
        # How many characters are there from the last indent stop:
        if lastStop == 0:
            indent_mod = tab_size
        else:
            indent_mod = lastStop % indent_size
            if not indent_mod:
                indent_mod = indent_size
        
        
        # Where should we stop:
        indentation_stop = max(0, indentation_length - indent_mod)

        # Go back to the point where we want the indentation to stop
        trailing = 0
        while indentation_length > indentation_stop:
            trailing += 1
            indentation = indentation[:-1]
            indentation_length = indentation.replace(" " * tab_size, "\t")
            indentation_length = indentation_length.replace(" \t", "\t").replace("\t", " " * tab_size)
            indentation_length = len(indentation_length)

        # Maybe add spaces if it needs some
        tab = " " * (indentation_stop - indentation_length)

        # Do actual unindent
        if trailing:
            indentation_region = sublime.Region(start_point - trailing, start_point)
            self.view.erase(edit, indentation_region)
        if tab:
            self.view.insert(edit, start_point - trailing, tab)

    def run(self, edit):
        sel = self.view.sel()
        for region in reversed(sel):
            for line in reversed(self.view.lines(region)):
                if line.a != line.b:
                    start = self.view.find("[^ \t]", line.begin())
                    if start is None:
                        start = line
                    self.unindent(edit, line, start)


class BackspaceSizeCommand(UnindentSizeCommand):
    def run(self, edit):
        sel = self.view.sel()
        for region in reversed(sel):
            if region.empty():
                for line in reversed(self.view.lines(region)):
                    if line.a != line.b:
                        start = self.view.find("[^ \t]", line.begin())
                        if start is None:
                            start = line
                        if region.begin() > start.begin() or region.begin() == line.begin():
                            self.view.erase(edit, sublime.Region(region.begin() - 1, region.end()))
                        else:
                            self.unindent(edit, line, region)
                    else:
                        self.view.erase(edit, sublime.Region(region.begin() - 1, region.end()))
            else:
                self.view.erase(edit, sublime.Region(region.begin(), region.end()))
