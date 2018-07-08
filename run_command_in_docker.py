import os
import re
import functools
import sublime
import string
import sublime_plugin

class ShowInPanel:
  def __init__(self, window):
    self.window = window

  def display_results(self):
    self.panel = self.window.get_output_panel("exec")
    self.window.run_command("show_panel", {"panel": "output.exec"})


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
    self.run_shell_command('docker exec $(basename $(pwd) | xargs -I % echo "tbb_playpen_inventory-api_run_1") npm run test')




