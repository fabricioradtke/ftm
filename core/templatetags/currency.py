from django.template import Library
import re


register = Library()

@register.filter
def money(value):

	try:
		value = float(value)
	except:
		return value

	orig = '%.2f' % (value)
	intpart, dec = orig.split('.')

	intpart = currency(intpart)

	return 'R$ ' + ','.join([intpart, dec])


@register.filter
def currency(value):

	orig = str(value)
	novo = re.sub(r'^(-?\d+)(\d{3})', '\g<1>.\g<2>', orig)

	if orig == novo:
		return novo

	return currency(novo)
