from src.core.infra.repo.meilsearchrepo import MeiliSearchRepository


class ProductMeiliSearchEngineRepo(MeiliSearchRepository):
    INDEX = "product-index"
    SEARCH_FIELDS = [
        "name",
        "brand",
        "groups",
        "category",
    ]
    FIELDS_TO_GET = ["id"]
