from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.folders import (
    Folder,
    CreateFolderRequest,
    UpdateFolderRequest,
)
from nylas.models.response import Response, ListResponse, DeleteResponse


class Folders(
    ListableApiResource,
    FindableApiResource,
    CreatableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(self, identifier: str) -> ListResponse[Folder]:
        """
        Return all Folders.

        Args:
            identifier: The identifier of the Grant to act upon.

        Returns:
            The list of Folders.
        """

        return super(Folders, self).list(
            path=f"/v3/grants/{identifier}/folders",
            response_type=Folder,
        )

    def find(self, identifier: str, folder_id: str) -> Response[Folder]:
        """
        Return a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            folder_id: The ID of the Folder to retrieve.

        Returns:
            The Folder.
        """
        return super(Folders, self).find(
            path=f"/v3/grants/{identifier}/folders/{folder_id}",
            response_type=Folder,
        )

    def create(
        self, identifier: str, request_body: CreateFolderRequest
    ) -> Response[Folder]:
        """
        Create a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            request_body: The values to create the Folder with.

        Returns:
            The created Folder.
        """
        return super(Folders, self).create(
            path=f"/v3/grants/{identifier}/folders",
            response_type=Folder,
            request_body=request_body,
        )

    def update(
        self, identifier: str, folder_id: str, request_body: UpdateFolderRequest
    ) -> Response[Folder]:
        """
        Update a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            folder_id: The ID of the Folder to update.
            request_body: The values to update the Folder with.

        Returns:
            The updated Folder.
        """
        return super(Folders, self).update(
            path=f"/v3/grants/{identifier}/folders/{folder_id}",
            response_type=Folder,
            request_body=request_body,
        )

    def destroy(self, identifier: str, folder_id: str) -> DeleteResponse:
        """
        Delete a Folder.

        Args:
            identifier: The identifier of the Grant to act upon.
            folder_id: The ID of the Folder to delete.

        Returns:
            The deletion response.
        """
        return super(Folders, self).destroy(
            path=f"/v3/grants/{identifier}/folders/{folder_id}"
        )
