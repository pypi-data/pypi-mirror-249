<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_etymology_plugin import models %>
<%! active_menu_item = "borrowings" %>


<h2> Borrowings </h2>

<div>
    ${ctx.render()}
</div>

## ${h.link(request, ctx.language)} ${ctx.name} ‘${h.link(request, ctx.meanings[0].meaning)}’

## <div class="tabbable">
##     <ul class="nav nav-tabs">
##         % if gloss_sentences:
##             <li class=${'active' if gloss_sentences else ''}><a href="#corpus" data-toggle="tab"> Corpus tokens </a></li>
##         % endif
##         % if ctx.formslices:
##             <li class=${'' if gloss_sentences else 'active'}><a href="#forms" data-toggle="tab"> Wordforms </a></li>
##         % endif
##         % if ctx.stemslices:
##             <li class=${'' if gloss_sentences or ctx.formslices else 'active'}><a href="#stems" data-toggle="tab"> Stems </a></li>
##         % endif
##     </ul>

##     <div class="tab-content" style="overflow: visible;">

##         <div id="forms" class="tab-pane ${'' if gloss_sentences else 'active'}">
##             <ul>
##                 % for fslice in ctx.formslices:
##                     <li> ${h.link(request, fslice.form)} </li>
##                 % endfor
##             </ul>
##         </div>

##         <div id="stems" class="tab-pane ${'' if gloss_sentences or ctx.formslices else 'active'}">
##             <ul>
##                 % for sslice in ctx.stemslices:
##                     <li> ${h.link(request, sslice.stem)} </li>
##                 % endfor
##             </ul>
##         </div>

##         <div id="corpus" class="tab-pane ${'active' if gloss_sentences else ''}">
##             % for gloss, sentences in gloss_sentences.items():
##                 <div id=${gloss}>
##                     % if len(sentences) > 1:
##                         <h5> As ‘${gloss}’:</h5>
##                     % endif
##                     ## <button type="button" class="btn btn-outline-info" onclick="copyIDs('${gloss}-ids')">Copy sentence IDs</button>
##                     <% stc_ids = [] %>
##                     <ol class="example">
##                         % for sentence in sentences:
##                             % if sentence.id not in stc_ids:
##                                 ${rendered_sentence(request, sentence, sentence_link=True)}
##                                 <% stc_ids.append(sentence.id) %>
##                             % endif
##                         % endfor
##                     </ol>
##                 </div>
##                 <script>
##                     var highlight_div = document.getElementById("${gloss}");
##                     var highlight_targets = [];
##                     % for x in ctx.allomorphs:
##                         highlight_targets.push(...highlight_div.querySelectorAll("*[name='${x.id}']"))
##                     % endfor
##                     console.log(highlight_targets)
##                     for (index = 0; index < highlight_targets.length; index++) {
##                         highlight_targets[index].classList.add("morpho-highlight");
##                     }
##                 </script>
##             % endfor
##         </div>
##     </div>  
## </div>

## <dl>
## % for key, objs in h.groupby(ctx.data, lambda o: o.key):
## <dt>${key}</dt>
##     % for obj in sorted(objs, key=lambda o: o.ord):
##     <dd>${obj.value}</dd>
##     % endfor
## % endfor
## </dl>
