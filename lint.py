import glob, re

def throw(filename, lineno, line, problem):
    print('===============')
    print('Exception in', filename, 'line', lineno)
    print(line)
    print(problem)

files = []
for filename in glob.iglob('/raw/**/*.md', recursive=True):
     files.append(filename)

for filename in files:
    with open(filename) as f:
      
        codeblock = 0
        enumstep = 0
        prev = None
        lineno = 1
        stepmarker = re.compile("^([0-9]\.)")

        for line in f:

            # code fences need a blank line around them
            if prev is not None:
                if '```' in line and not codeblock and not prev.isspace():
                    throw(filename, lineno, line, 'Code blocks need a blank line before')
                if '```' in prev and not codeblock and not line.isspace():
                    throw(filename, lineno, line, 'Code blocks need a blank line after')

            # are we inside a code block?
            if "```" in line:
                codeblock = (codeblock + 1)%2

            # are we inside an enumerated step?
            if stepmarker.match(line) and not codeblock:
                enumstep = 1
            if re.compile("^#").match(line):
                enumstep = 0

            # no double blank lines inside code blocks
            if codeblock == 1 and prev.isspace() and line.isspace():
                throw(filename, lineno, line, 'No double blank lines allowed in code blocks')

            # steps 1-9 need two spaces after the dot
            if not codeblock and stepmarker.match(line):
                if line[2:4] != '  ':
                    throw(filename, lineno, line, 'Step numbers "1." through "9." need to be followed by two spaces, ie "4.<space><space>"')

            # four-space indent inside enumerated steps (but not in code blocks):
            if enumstep == 1 and codeblock == 0:
                pattern = re.compile("^(    [a-zA-Z0-9*-`!(].)")
                if not pattern.match(line) and not (stepmarker.match(line) or re.compile("^([0-9][0-9]\.)").match(line)) and not line.isspace():
                    throw(filename, lineno, line, 'Text in an enumerated step should be indented by 4 spaces')

            lineno += 1
            prev = line
         
        # must end in newline
        if line[-1] != '\n':
            throw(filename, lineno-1, line, 'md file must end in newline') 
