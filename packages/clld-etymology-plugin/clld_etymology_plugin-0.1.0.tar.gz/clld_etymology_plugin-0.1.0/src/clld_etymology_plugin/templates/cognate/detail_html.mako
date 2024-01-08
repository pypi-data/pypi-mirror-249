<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>


<h3>${_('Cognate set')}</h3>

% if ctx.contribution:
    From contribution: ${h.link(request, ctx.contribution)}
% endif

<%util:table items="${ctx.reflexes}" args="item" options="${dict(bInfo=True)}">
    <%def name="head()">
        <th>Form</th>
        <th>Language</th>
        <th>Alignment</th>
    </%def>
    <td>${h.link(request, item.counterpart)}</td>
    <td>${h.link(request, item.counterpart.language)}</td>
    <td>
        <span class="alignment">${item.alignment}</span>
    </td>
</%util:table>

<script src="http://127.0.0.1:6543/static/alignment.js"></script>
<link rel="stylesheet" href="http://127.0.0.1:6543/static/alignment.css" type="text/css"/>
<script>
    $( document ).ready(function() {
        var alignments = document.getElementsByClassName("alignment");
        for (var i=0,alignment; alignment=alignments[i]; i++) {
            alignment.innerHTML = plotWord(alignment.innerHTML, 'span');
        }
    });
</script>