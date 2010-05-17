from chameleon.genshi import template

def render(fileName):
    t = template.GenshiTemplateFile(fileName, debug=True)
    body = t.render()
    return body

