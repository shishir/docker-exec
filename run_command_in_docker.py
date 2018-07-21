import os
import re
import functools
import sublime
import string
import re
import sublime_plugin

class ShowInPanel:
  def __init__(self, window):
    self.window = window

  def display_results(self):
    self.window().show_quick_panel(quick.exec, self.done)


class BaseTask(sublime_plugin.TextCommand):

  def run_shell_command(self, command, working_dir="."):
    if not command:
      return False
    self.view.window().run_command("exec", {
      "cmd": command,
      "shell": True,
      "working_dir": working_dir,
    })
    self.display_results()
    return True

  def display_results(self):
    display = ShowInPanel(self.window())
    display.display_results()

  def window(self):
    return self.view.window()

class DockerExec(BaseTask):
  def isEnabled(view, args):
    return True
  def run(self, args):
    self.view.window().show_input_panel(
        "Comand", "npm run test",
        self.execute, None, None
    )
  def execute(self, usr_cmd):
    path = self.view.file_name().split("/")
    print(path)
    component_name = path[path.index("components") + 1];
    command = "docker exec tbb_playpen_"+component_name+"_run_1 "+usr_cmd
    self.run_shell_command(command)

class ToggleTest(BaseTask):
  def isEnabled(view, args):
    return True
  def run(self, args):
    file_name_arr = os.path.basename(self.view.file_name()).split(".")
    if file_name_arr[-2] == 'spec':
      file_name = file_name_arr[0] + '.ts'
    else:
      file_name = file_name_arr[0] + '.spec.ts'
    new_file_name = os.path.dirname(self.view.file_name()) + "/"+file_name
    if os.path.exists(new_file_name):
      self.view.window().open_file(new_file_name)
    else:
      create(new_file_name)
      print('Not Found')
