from pydantic import BaseModel, RootModel

class EstablishmentEntryModel(BaseModel):
    name: str
    homepage: str
    linkOnly: bool

class EstablishmentEntriesModel(RootModel):
    root: dict[str, EstablishmentEntryModel]
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "bo-asi": {
                    "name": "Bo Asi!",
                    "homepage": "https://www.boasi.cz",
                    "linkOnly": False
                }, 
                "hodonanka":{
                    "name": "Hodoňanka", 
                    "homepage": "https://www.rozvoz-jidla-ostrava.cz", 
                    "linkOnly": False
                }
            }]
        }
    }