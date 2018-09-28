from django import template

register = template.Library()

@register.simple_tag(name='get_fields_from_row')
def get_fields_from_row(row, col_names, width=70):
    result = []
    for col in col_names:
        try:
            val = getattr(row,col[0])
            if col[1] and val:
                if width:
                    width = f' width="{int(width)}"'
                val = f'<img src="/media/{val}" {width}/>'
            result.append(val) 
        except AttributeError:
            pass
    return result

@register.simple_tag(name='get_m2m_fields_from_row')
def get_m2m_fields_from_row(row, col_names):
    result = []
    for col in col_names:
        try:
            attr_ = getattr(row,col)
            attr_name_ = attr_.model._meta.verbose_name_plural
            result.append([attr_name_,attr_])
        except AttributeError:
            pass
    return result
