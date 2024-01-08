<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<%! from clld_etymology_plugin.util import build_tree, etymology %>
<%! active_menu_item = "cognatesets" %>

## <%def name="sidebar()">
##     <%util:well title="${_('Distribution')}">

##     </%util:well>
## </%def>


<h3>${_('Cognate set')} ${ctx.description}</h3>

<% tree = build_tree(request, ctx) %>

<div class="row-fluid">
  <div class="span12">
    <div class="row-fluid">
    % if len(tree) > 25 or ctx.contribution or ctx.source:
        <div class="span6">
            <table class="table table-nonfluid">
                <tbody>
                    % if ctx.contribution:
                        <tr>
                            <td>Contribution:</td>
                            <td>${h.link(request, ctx.contribution)}</td>
                        </tr>
                    % endif
                    % if ctx.source:
                        <tr>
                            <td> Source:</td>
                            <td>${h.link(request, ctx.source)}</td>
                        </tr>
                    % endif
                    % if len(tree) > 25:
                        <tr>
                            <td> Overview:</td>
                            <td>${tree|n}</td>
                        </tr>
                    % endif
               </tbody>
            </table>
        </div>
    % endif
% if map_ or request.map:
      <div class="span6">${(map_ or request.map).render()}</div>
% endif
    </div>
  </div>
</div>

<h4>${_('Aligned cognates')}</h4>

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

<script src="${req.static_url('clld_etymology_plugin:static/alignment.js')}"></script>
<link rel="stylesheet" href="${req.static_url('clld_etymology_plugin:static/alignment.css')}" type="text/css"/>
<script>
    $( document ).ready(function() {
        var alignments = document.getElementsByClassName("alignment");
        for (var i=0,alignment; alignment=alignments[i]; i++) {
            alignment.innerHTML = plotWord(alignment.innerHTML, 'span');
        }
    });
</script>

## <div style="position: absolute; width: 100%; left: 0;">


## </div>