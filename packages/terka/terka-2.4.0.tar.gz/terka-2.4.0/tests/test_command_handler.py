from terka.entrypoints.cli import  _CommandHandler


class TestCommandHandler:

    def test_command_handler_populates_created_by_for_new_task(self, bus):
        command_handler = _CommandHandler(bus)
        task_dict = {"name": "test_task"}
        task_dict = command_handler.update_task_dict(task_dict)
        assert task_dict.get("created_by") == bus.config.get("user")

    def test_command_handler_populates_workspace_for_new_project(self, bus):
        command_handler = _CommandHandler(bus)
        task_dict = {"name": "test_project"}
        task_dict = command_handler.update_task_dict(task_dict)
        assert task_dict.get("workspace") == bus.config.get("workspace")

