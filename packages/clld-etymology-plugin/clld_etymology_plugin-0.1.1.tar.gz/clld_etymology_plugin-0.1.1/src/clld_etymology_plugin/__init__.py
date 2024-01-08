from clld_etymology_plugin import adapters, datatables, interfaces, maps, models


def includeme(config):
    config.registry.settings["mako.directories"].insert(
        1, "clld_etymology_plugin:templates"
    )
    config.add_static_view(
        "clld-etymology-plugin-static", "clld_etymology_plugin:static"
    )

    config.register_resource(
        "cognateset", models.Cognateset, interfaces.ICognateset, with_index=True
    )
    config.register_map("cognateset", maps.CognatesetMap)
    config.register_adapter(
        adapters.GeoJsonCognateset,
        interfaces.ICognateset,
        name=adapters.GeoJsonCognateset.mimetype,
    )

    config.register_resource(
        "borrowing", models.Borrowing, interfaces.IBorrowing, with_index=True
    )
    config.register_datatable("borrowings", datatables.Borrowings)
