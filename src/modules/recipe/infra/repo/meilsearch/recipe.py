from src.core.infra.repo.meilsearchrepo import MeiliSearchRepository


class RecipeMeiliSearchEngineRepo(MeiliSearchRepository):
    INDEX = "recipe-index"
    SEARCH_FIELDS = [
        "name",
        "description",
    ]
    FIELDS_TO_GET = ["id"]
