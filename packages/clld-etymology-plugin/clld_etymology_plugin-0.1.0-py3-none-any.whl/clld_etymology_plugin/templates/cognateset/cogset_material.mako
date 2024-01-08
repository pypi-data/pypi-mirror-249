

#Contribution: ${h.link(request, ctx.contribution)} by
#% for contributor in ctx.contribution.primary_contributors:
#${h.link(request, contributor)}
#% endfor
#<br>
#${ctx.description}

#<%util:table items="${ctx.reflexes}" args="item" options="${dict(bInfo=True)}">
#    <%def name="head()">
#        <th>Morpheme</th>
#        <th>Meaning(s)</th>
#        <th>Language</th>
#        <th>Alignment</th>
#    </%def>
#    <td>${h.link(request, item.counterpart)}</td>
#    <td>
#
#    % for morpheme_meaning in item.counterpart.meanings:
#        ‘${h.link(request, morpheme_meaning.meaning)}’
#    % endfor
#    </td>
#    <td>${h.link(request, item.counterpart.language)}</td>
#    <td>
#        <span class="alignment">${item.alignment}</span>
#    </td>
#</%util:table>