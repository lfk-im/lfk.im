---
layout: home
---

<ul>
{% for place in site.places %}
<li>{{ place.name }}</li>
{% endfor %}
</ul>
