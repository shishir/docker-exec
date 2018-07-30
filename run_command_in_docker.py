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
    self.panel = self.window.get_output_panel("exec")
    self.panel.set_syntax_file("Packages/ANSIescape/ANSI.tmLanguage")
    self.panel.set_read_only(True)
    self.window.run_command("show_panel", {"panel": "output.exec"})

    # self.window().show_quick_panel(quick.exec)


class BaseTask(sublime_plugin.TextCommand):

  def run_shell_command(self, command, working_dir="."):
    if not command:
      return False
    self.view.window().run_command("exec", {
      "cmd": command,
      "shell": True,
      "working_dir": working_dir,
      "encoding": "utf-8"
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
    component_name = path[path.index("components") + 1];
    command = "docker exec tbb_playpen_"+component_name+"_run_1 "+usr_cmd
    self.run_shell_command(command)

class ToggleTest(BaseTask):
  def isEnabled(view, args):
    return True
  def run(self, args):
    file_name_arr = os.path.basename(self.view.file_name()).split(".")
    if file_name_arr[-2] == 'spec' or file_name_arr[-2] == 'int':
      file_name = file_name_arr[0] + '.ts'
      new_file_name = os.path.dirname(self.view.file_name()) + "/"+file_name
    else:
      file_name = file_name_arr[0] + '.spec.ts'
      new_file_name = os.path.dirname(self.view.file_name()) + "/"+file_name
      if not os.path.exists(new_file_name):
        file_name = file_name_arr[0] + '.int.spec.ts'
        new_file_name = os.path.dirname(self.view.file_name()) + "/"+file_name
    if os.path.exists(new_file_name):
      self.view.window().open_file(new_file_name)
    else:
      print('Not Found')

class RunTest(BaseTask):
  def isEnabled(view, args):
    return True
  def run(self, args):
    file_name = self.view.file_name()
    cmd = "node_modules/.bin/jest "
    if self.isSpecFile(file_name):
      cmd = cmd + self.spec_name(file_name)
    else:
      fname = self.construct_spec_file_name(file_name)
      cmd = cmd + fname
    print("cmd:",cmd)
    command = "docker exec -t tbb_playpen_"+self.component_name(file_name)+"_run_1 "+cmd + "  --no-colors --no-coverage"
    self.run_shell_command(command)

  def component_name(self, file_name):
    path = file_name.split("/")
    component_name = path[path.index("components") + 1];
    return component_name
  def spec_name(self, file_name):
    dirname = os.path.dirname(file_name).split("/")
    name = os.path.join(*dirname[(dirname.index("components") + 2):]) +"/"+os.path.basename(file_name)
    return name
  def isSpecFile(self, file_name):
    file_name_arr = os.path.basename(file_name).split(".")
    return (file_name_arr[-2] == 'spec') or (file_name_arr[-2] == 'int')

  def specFileExists(self, file_name):
    print("specFileExists", file_name)
    return os.path.isfile(file_name)

  def construct_spec_file_name(self, file_name):
    dirname = os.path.dirname(file_name).split("/")
    file_name_arr = os.path.basename(file_name).split(".")
    # print(file_name)
    spec_file_name = file_name_arr[0] + '.spec.ts'
    if os.path.isfile((os.path.dirname(file_name) + "/"+spec_file_name)):
      return os.path.join(*dirname[(dirname.index("components") + 2):]) +"/"+os.path.basename(spec_file_name)
    spec_file_name = file_name_arr[0] + ".int.spec.ts"
    if os.path.isfile((os.path.dirname(file_name) + "/"+spec_file_name)):
      return os.path.join(*dirname[(dirname.index("components") + 2):]) +"/"+os.path.basename(spec_file_name)





