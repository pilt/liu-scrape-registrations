# coding=utf-8

def summary(dump):
    course_names = dump['course_names']
    course_regs = dump['course_regs']
    course_reg_counts = dump['course_reg_counts']
    listed = [(code, num) for code, num in course_reg_counts.items()]
    listed.sort(key=lambda x: x[1], reverse=True)
    outs = []
    for code, regs in listed:
        out = u"%5s  %s (%s)" % (regs, course_names[code], code)
        outs.append(out.encode('utf-8'))
    outs.append('')
    return "\n".join(outs)
