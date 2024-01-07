from serenity_sdk.api.core import CallType, SerenityApi, SerenityClient
from serenity_types.storage.core import DatasetContent, DatasetContentUrlAndToken


class StorageApi(SerenityApi):
    """
    Helper class for the Storage API, which lets clients generate URL and token to
    access Serenity generated files.
    """

    def __init__(self, client: SerenityClient):
        """
        :param client: the raw client to delegate to when making API calls
        """

        # NOTE: I don't think the base endpoint should be valuation in the future but
        # understand this is the most practical arrangement to start; however, the
        # SDK client at least should be independent from valuation.
        super().__init__(client, "org/storage")

    def get_ctm_download_url_and_token(
        self, dataset_content: DatasetContent
    ) -> DatasetContentUrlAndToken:
        """
        Generates the URL and SAS token to access the specified dataset content.
        """
        raw_json = self._call_api(
            api_path=f"/downloadurl/{dataset_content.value}",
            call_type=CallType.GET,
        )
        return DatasetContentUrlAndToken.parse_obj(raw_json["result"])
