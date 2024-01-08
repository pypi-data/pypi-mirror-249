from clld.web.maps import Layer, Map


class CognatesetMap(Map):
    def get_layers(self):
        yield Layer(
            self.ctx.id, self.ctx.name, self.req.resource_url(self.ctx, ext="geojson")
        )

    def get_default_options(self):
        return {
            "show_labels": True,
            "info_query": {"cognateset": self.ctx.pk},
            "hash": True,
            "max_zoom": 19,
        }
