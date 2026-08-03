from pydantic import BaseModel, RootModel

class EstablishmentEntryResponse(BaseModel):
    name: str
    homepage: str
    linkOnly: bool

class EstablishmentEntriesResponse(RootModel):
    root: dict[str, EstablishmentEntryResponse]
    
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