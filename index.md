---
layout: none
---

<div>
{% for place in site.places %}
<div>
{{ place.name }} 
{{ place.address }}
{{ place.hours }}
{{ place.restaurant_phone }}
{{ place.takeout }}
{{ place.curbside }}
{{ place.delivery }}
</div>
<hr>
{% endfor %}
</div>
