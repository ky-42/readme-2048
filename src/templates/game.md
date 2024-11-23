<h3 align="center">2048</h3>
<p align="center">
  The current score is 24{% if end_date is not none %} and the highscore is {{ highscore }} which was set on {{ end_date }}.{% else %}.{% endif %}
</p>

<p align="center">
  &nbsp;&nbsp;
  <a href="{{server_address}}/click/3">Left</a>
  &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="{{server_address}}/click/1">Up</a>
  &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="{{server_address}}/click/4">Right</a>
</p>

<table align="center">
{% for grid_row in grid %}
<tr>
{% for block in grid_row %}
<td align="center">
  </br>
  <strong>{{ block }}</strong>
  </br>
  <img width="58" height="0">
</td>
{% endfor %}
</tr>
{% endfor %}
</table>

<p align="center"><a href="{{server_address}}/click/2">Down</a></p>