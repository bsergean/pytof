import re

def fix1(fn):
    lines = open(fn).read().splitlines()
    i = 0
    while True:
        if i >= len(lines):
            break
        line = lines[i]

        hit = re.match('^\s+foo\(', line)
        if hit:
            while ');' not in line:
                i += 1
                line += lines[i]
            i += 1
            print line
            continue

        print line
        i += 1

def fix2(fn):
    lines = open(fn).read().splitlines()
    i = 0
    while True:
        if i >= len(lines):
            break
        line = lines[i]

        hit = line.find('foo(')
        if hit >= 0:
            line = line.strip()
            end = line.find(');')
            line = line[0:end]

            tokens = line.split(',')
            if 'TOTO' in tokens[2]: t = 'toto'
            elif 'TATA' in tokens[2]: t = 'tata'

            line = hit * ' '
            fmt = re.search(r'"(.*)"', tokens[3]).group(1)
            if len(tokens) > 4:
                line += 'throw %s("%s");' % (t, fmt)
            else:
                if '%d' in fmt: fmt = re.sub('%d', '%%', fmt)
                if '%s' in fmt: fmt = re.sub('%s', '%%', fmt)

                line += 'throw %s(str(format("%s", ' % (t, fmt)
                line += '%s)));' % (', '.join(t.strip() for t in tokens[4:]))
            i += 1
            print line
            continue

        print line
        i += 1

# fix1('regplace.txt')
fix2('regplace2.txt')
