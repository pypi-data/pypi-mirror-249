from clld import interfaces
from clld.web.adapters.geojson import GeoJson

# https://github.com/clld/clld-cognacy-plugin/blob/42c0cd4beee392d14e698bf6430bbb4c4e2f33ad/src/clld_cognacy_plugin/adapters.py#L10


class GeoJsonCognateset(GeoJson):
    def featurecollection_properties(self, ctx, req):
        marker = req.registry.getUtility(interfaces.IMapMarker)
        return {
            "name": getattr(ctx, "name", "Units"),
            "domain": [
                {"icon": marker(de, req), "id": de.id, "name": de.name}
                for de in getattr(ctx, "domain", [])
            ],
        }

    def feature_iterator(self, ctx, req):
        return [cognate.counterpart for cognate in ctx.units]

    def get_language(self, ctx, req, unit):
        return unit.language

    def feature_properties(self, ctx, req, unit):
        return {"label": unit.name}
