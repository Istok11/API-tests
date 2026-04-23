from faker import Faker

from src.models.issues import CreateIssueRequest, EditIssueRequest

faker = Faker()

class IssuesFactory:
    @staticmethod
    def build_create(**overrides) -> CreateIssueRequest:
        data = {
            "title": faker.word(),
            "description": faker.text(),
            "priority": "medium",
            "assignee_id": None,
        }

        data.update(overrides)
        return CreateIssueRequest(**data)

    def build_edit(**overrides) -> EditIssueRequest:
        data = {
            "title": faker.word(),
            "description": faker.text(),
            "priority": "medium",
            "assignee_id": None,
        }

        data.update(overrides)
        return EditIssueRequest(**data)

