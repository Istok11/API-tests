import pytest
import requests
import os
import json

from src.data.auth_factory import RegisterFactory
from src.data.issues_factory import IssuesFactory
from src.models.issues import Status, ChangeStatusIssueRequest


# -- AUTH --
def test_successful_registration(auth_client):
    request = RegisterFactory.build()
    user = auth_client.register(request)

    assert user.id is not None
    assert user.email == request.email
    assert user.role == request.role
    assert user.created_at is not None

# -- USERS --
def test_successful_get_me(users_client):
    request = users_client.get_me()
    user = users_client.get_me()

    assert user.id == request.id
    assert user.email == request.email
    assert user.role == request.role
    assert user.created_at is not None



# -- ISSUES --
def test_successful_get_list_issues(issue_client):
    request = IssuesFactory.build_create()
    created = issue_client.create_issue(request)

    issues = issue_client.get_issues()

    ids = [issue.id for issue in issues]

    assert created.id in ids


def test_successful_create_issue(issue_client):
    request = IssuesFactory.build_create()
    issue = issue_client.create_issue(request)

    assert issue.id is not None
    assert issue.title == request.title
    assert issue.priority == request.priority
    assert issue.description == request.description


def test_successful_get_issue_by_id(issue_client):
    request = IssuesFactory.build_create()
    created = issue_client.create_issue(request)

    issue_id = created.id
    issue = issue_client.get_issue(issue_id)

    assert issue.id is not None
    assert issue.title == request.title
    assert issue.priority == request.priority
    assert issue.description == request.description

def test_successful_edit_issue(issue_client):
    created = issue_client.create_issue(IssuesFactory.build_create())

    update_request = IssuesFactory.build_edit()

    issue_client.edit_issue(created.id, update_request)

    updated = issue_client.get_issue(created.id)

    assert updated.title == update_request.title
    assert updated.priority == update_request.priority
    assert updated.description == update_request.description


def test_successful_delete_issue(issue_client):
    created = issue_client.create_issue(IssuesFactory.build_create())

    issue_client.delete_issue(created.id)

    issues = issue_client.get_issues()
    ids = [issue.id for issue in issues]

    assert created.id not in ids



@pytest.mark.parametrize("status", [
    Status.in_progress,
    Status.ready_for_qa,
    Status.qa,
    Status.done,
    Status.closed,
])
def test_successful_change_each_status(issue_client, status):
    created = issue_client.create_issue(IssuesFactory.build_create())

    issue_client.change_status(created.id,
                               ChangeStatusIssueRequest(new_status=status)
                               )

    updated = issue_client.get_issue(created.id)

    assert updated.status == status.value



def test_successful_get_meta_statuses(issue_client):
    statuses = issue_client.get_meta_statuses_for_qa()

    assert set(statuses.allowed_statuses).issubset(set(statuses.all_statuses))











