from nylas.handler.api_resources import (
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
)
from nylas.models.response import ListResponse, Response, DeleteResponse
from nylas.models.threads import ListThreadsQueryParams, Thread, UpdateThreadRequest


class Threads(
    ListableApiResource,
    FindableApiResource,
    UpdatableApiResource,
    DestroyableApiResource,
):
    def list(
        self, identifier: str, query_params: ListThreadsQueryParams
    ) -> ListResponse[Thread]:
        """
        Return all Threads.

        Args:
            identifier: The identifier of the grant to get threads for.
            query_params: The query parameters to filter threads by.

        Returns:
            A list of Threads.
        """
        return super(Threads, self).list(
            path=f"/v3/grants/{identifier}/threads",
            response_type=Thread,
            query_params=query_params,
        )

    def find(self, identifier: str, thread_id: str) -> Response[Thread]:
        """
        Return a Thread.

        Args:
            identifier: The identifier of the grant to get the thread for.
            thread_id: The identifier of the thread to get.

        Returns:
            The requested Thread.
        """
        return super(Threads, self).find(
            path=f"/v3/grants/{identifier}/threads/{thread_id}",
            response_type=Thread,
        )

    def update(
        self,
        identifier: str,
        thread_id: str,
        request_body: UpdateThreadRequest,
    ) -> Response[Thread]:
        """
        Update a Thread.

        Args:
            identifier: The identifier of the grant to update the thread for.
            thread_id: The identifier of the thread to update.
            request_body: The request body to update the thread with.

        Returns:
            The updated Thread.
        """
        return super(Threads, self).update(
            path=f"/v3/grants/{identifier}/threads/{thread_id}",
            response_type=Thread,
            request_body=request_body,
        )

    def destroy(self, identifier: str, thread_id: str) -> DeleteResponse:
        """
        Delete a Thread.

        Args:
            identifier: The identifier of the grant to delete the thread for.
            thread_id: The identifier of the thread to delete.

        Returns:
            The deletion response.
        """
        return super(Threads, self).destroy(
            path=f"/v3/grants/{identifier}/threads/{thread_id}",
        )
