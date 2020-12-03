from django import template

register = template.Library()

# scriptを置換して無効化するフィルタ
@register.filter
def sanitize(value):
    return value.replace('<script', '<pre').replace('</script', '</pre').replace('<style', '<pre').replace('</style', '</pre')
