establishment_list_schema = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "required": ["name", "homepage", "linkOnly"],
        "additionalProperties": False,
        "properties": {
            "name": {
                "type": "string",
                "description": "The display name of the establishment."
            },
            "homepage": {
                "type": "string",
                "format": "uri",
                "description": "The website URL of the establishment."
            },
            "linkOnly": {
                "type": "boolean",
                "description": "Flag to indicate if only the link should be displayed."
            }
        }
    }
}

establishment_list_example = {
    "bo-asi": {
        "name": "Bo Asi!",
        "homepage": "https://www.boasi.cz",
        "linkOnly": False
    },
    "paleta": {
        "name": "Paleta",
        "homepage": "https://www.paletarestaurant.cz",
        "linkOnly": False
    },
    "hodonanka": {
        "name": "Hodoňanka",
        "homepage": "https://www.rozvoz-jidla-ostrava.cz",
        "linkOnly": False
    },
    "phobo": {
        "name": "Pho Bo",
        "homepage": "https://www.facebook.com/p/PHO-BO-Restaurant-100082901603735",
        "linkOnly": True
    }
}

establishment_menu_schema = {
    "type": "object",
    "patternProperties": {
        "^(?:\\d{4}-\\d{2}-\\d{2}|week)$": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "price"],
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the item."
                    },
                    "price": {
                        "type": ["number", "null"],
                        "description": "Price of the item."
                    }
                },
            }
        }
    },
    "additionalProperties": False
}

establishment_menu_example = {
    "2026-01-26": [
        {
            "name": "Polévka bramboračka",
            "price": None
        },
        {
            "name": "Holandský řízek XXL 200g, máslová bramborová kaše, salátek",
            "price": 164
        },
        {
            "name": "Marinované kuřecí medailoky, pečené brambory ve slupce, tatarská omáčka",
            "price": 164
        },
    ],
    "2026-01-27": [
        {
            "name": "Polévka hrachová",
            "price": None
        },
        {
            "name": "Hovězí svíčková na smetaně, houskový knedlík, citron, brusinky",
            "price": 179
        },
        {
            "name": "Kuřecí prsíčko na středomořský způsob s rajčaty, olivami, kapary a česnekem, rýže",
            "price": 164
        }
    ],
    "week": [
        {
            "name": "Polévka rajská",
            "price": None
        },
        {
            "name": "Currywrust (německá specialita grilovaná klobása 200g s kořením ) s hranolky",
            "price": 164
        },
        {
            "name": "Holandský řízek XXL 200g, máslová bramborová kaše, salátek",
            "price": 164
        },
    ]
}

sanic_error_schema = {
    "type": "object",
    "additionalProperties": False,
    "required": ["description", "status", "message"],
    "properties": {
        "description": {
            "type": "string", 
            "description": "Name of the error."
        },
        "status": {
            "type": "number",
            "description": "HTTP error code."
        },
        "message": {
            "type": "string",
            "description": "Human readable error message."
        },
    }
}

establishment_doesnt_provide_menu_example = {
    "description": "Bad Request",
    "status": 400,
    "message": "Establishment \"phobo\" doesn't provide a menu"
}