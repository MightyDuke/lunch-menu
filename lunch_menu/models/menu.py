from pydantic import BaseModel, RootModel

class MenuItemResponse(BaseModel):
    name: str
    price: int | None
    highlight: bool | None

class MenuDayResponse(RootModel):
    root: list[MenuItemResponse]

class MenuForEstablishmentResponse(RootModel):
    root: dict[str, MenuDayResponse]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "2025-01-01": [
                        {
                            "name": "Holandský řízek podávaný s bramborovou kaší, sálátek",
                            "price": 159,
                            "highlight": False,
                        },
                        {
                            "name": "Grilovaný losos s máslovými noky a smetanovým listovým špenátem",
                            "price": 169,
                            "highlight": False
                        }
                    ],
                    "2025-01-02": [
                        {
                            "name": "Polévka gulášová",
                            "price": None,
                            "highlight": False
                        },
                        {
                            "name": "Domácí bramborový placek s masovou směsí dvou barev sypaný sýrem gouda",
                            "price": 159,
                            "highlight": True
                        }
                    ]
                }
            ]
        }
    }

class HighlightedWordsResponse(RootModel):
    root: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                [
                    "prejt", "kari", "low carb"
                ]
            ]
        }
    }