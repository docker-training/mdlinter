import glob, re

def throw(filename, lineno, line, problem):
    course = filename.split('/')[2]
    print(course, '===============')
    print(course, 'Exception in', filename, 'line', lineno)
    print(course, line)
    print(course, problem)

files = []

for filename in glob.iglob('/raw/**/*.md', recursive=True):
     files.append(filename)

for filename in files:
    with open(filename) as f:
      
        codeblock = 0
        prev_codeblock = 0
        enumstep = 0
        prev_enumstep = 0
        bullets = 0
        prev_bullets = 0
        command = 0
        prev_command = 0
        yamlhead = 0
        prev_yamlhead = 0
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

            # are we inside a bullet list?
            if not codeblock and len(line.lstrip())>1 and line.lstrip()[0:2] == '- ':
                bullets = 1
            else:
                bullets = 0

            # are we inside a yaml header?
            if not codeblock and "---" in line:
                yamlhead = (yamlhead + 1)%2

            # bullet lists need a blank line around them at top level
            if (not enumstep or not prev_enumstep) and (not codeblock or not prev_codeblock) and (not yamlhead or not prev_yamlhead):
                if bullets and not prev_bullets and not prev.isspace():
                    throw(filename, lineno, line, 'Bullet lists need a blank line before')
                elif prev_bullets and not bullets and not line.isspace():
                    throw(filename, lineno, line, 'Bullet lists need a blank line after')
  
            # no double blank lines
            if prev is not None and prev.isspace() and line.isspace():
                throw(filename, lineno, line, 'No double blank lines')

            # steps 1-9 need two spaces after the dot
            if not codeblock and stepmarker.match(line):
                if line[2:4] != '  ':
                    throw(filename, lineno, line, 'Step numbers "1." through "9." need to be followed by two spaces, ie "4.<space><space>"')

            # four-space indent inside enumerated steps (but not in code blocks), more spaces ok for lists:
            if enumstep == 1 and codeblock == 0:
                pattern = re.compile("^( {4}[a-zA-Z0-9*-`!(|)].)")
                listpattern = re.compile("^[ ]{4,}-")
                if not pattern.match(line) and not listpattern.match(line) and not (stepmarker.match(line) or re.compile("^([0-9][0-9]\.)").match(line)) and not line.isspace():
                    throw(filename, lineno, line, 'Text in an enumerated step should be indented by 4 spaces')

            # is this line part of a command?
            if 'centos@' in line or 'ubuntu@' in line or re.compile("PS:.*>").match(line.lstrip()) or (prev_command and (prev.rstrip()[-1] == '\\' or prev.rstrip()[-1] == '`')):
                command = 1
            else:
                command = 0

            # codeblocks maximum 95 char
            if codeblock and len(line.rstrip()) > 95:
                throw(filename, lineno, line, 'Code blocks must be <= 95 characters')

            # figures end with /
            if re.compile("!\[.*\]\(.*\)").match(line.lstrip()) and line.rstrip()[-1] is not '/':
                throw(filename, lineno, line, 'Figures must end with /')

            lineno += 1
            prev = line
            prev_codeblock = codeblock
            prev_yamlhead = yamlhead
            prev_enumstep = enumstep
            prev_bullets = bullets
            prev_command = command
         
        # must end in newline
        if line[-1] != '\n':
            throw(filename, lineno-1, line, 'md file must end in newline') 
