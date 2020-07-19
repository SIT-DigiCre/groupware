from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

# 配列の中身を変数によりアクセスする
# （デフォルトのテンプレートタグでは出来なかったので、カスタムタグを作成）
@register.simple_tag
def check(value1, value2):
    return value1[value2]