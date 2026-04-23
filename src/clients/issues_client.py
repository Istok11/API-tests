import requests

from .base_client import BaseClient
from ..models.issues import (CreateIssueRequest, IssueResponse, EditIssueRequest, ChangeStatusIssueRequest,
DeleteIssueResponse, MetaStatusesForQaResponse)


class IssueClient(BaseClient):

    def get_issues(self) -> list[IssueResponse]:
        response = self.get("/api/issues")

        assert response.status_code == 200, response.text

        return [IssueResponse(**item) for item in response.json()]


    def create_issue(self, request: CreateIssueRequest) -> IssueResponse:
        response = self.post(
            "/api/issues",
            json=request.model_dump()
        )
        assert response.status_code == 200, response.text
        return IssueResponse(**response.json())


    def get_issue(self, issue_id: int) -> IssueResponse:
        response = self.get(f"/api/issues/{issue_id}")

        assert response.status_code == 200, response.text

        return IssueResponse(**response.json())


    def edit_issue(self,issue_id, request: EditIssueRequest) -> IssueResponse:
        response = self.put(
            f"/api/issues/{issue_id}",
            json=request.model_dump()
        )
        assert response.status_code == 200, response.text
        return IssueResponse(**response.json())

    def delete_issue(self, issue_id: int):
        response = self.delete(f"/api/issues/{issue_id}")

        assert response.status_code == 200, response.text
        return DeleteIssueResponse(**response.json())

    def change_status(self, issue_id: int, request: ChangeStatusIssueRequest) -> IssueResponse:
        response = self.post(
            f"/api/issues/{issue_id}/status",
            json=request.model_dump()
        )
        assert response.status_code == 200, response.text
        return IssueResponse(**response.json())

    def get_meta_statuses_for_qa(self) -> MetaStatusesForQaResponse:
        response = self.get(
            f"/api/issues/meta/statuses")
        assert response.status_code == 200, response.text
        return MetaStatusesForQaResponse(**response.json())



