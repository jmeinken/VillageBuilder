from django import template
from datetime import date, timedelta

register = template.Library()





@register.filter(name='label_with_classes', is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter(name='remove_colon', is_safe=True)
def remove_colon(value):
    return value.replace(':','')

@register.filter('field_type')
def field_type(ob):
    if ob.__class__.__name__ == 'BoundField':
        return ob.field.__class__.__name__
    else:
        return ob.__class__.__name__


# use like this: {% make_list var1 var2 var3 as some_list %}

@register.tag
def make_list(parser, token):
  bits = list(token.split_contents())
  if len(bits) >= 4 and bits[-2] == "as":
    varname = bits[-1]
    items = bits[1:-2]
    return MakeListNode(items, varname)
  else:
    raise template.TemplateSyntaxError("%r expected format is 'item [item ...] as varname'" % bits[0])

class MakeListNode(template.Node):
  def __init__(self, items, varname):
    self.items = map(template.Variable, items)
    self.varname = varname

  def render(self, context):
    context[self.varname] = [ i.resolve(context) for i in self.items ]
    return ""