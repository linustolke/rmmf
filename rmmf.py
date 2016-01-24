from __future__ import print_function
import re
import os

class Goal:
    goal_regex = re.compile(r"""(.PHONY ?: (.*)
)?(.*) ?: ?((.|\\
)*)
((	..*
)*)""")

    def __init__(self, match):
        self.goals = match.group(3).strip()
        assert " " not in self.goals
        if match.group(2):
            assert match.group(2) == self.goals, "Restriction: phony declaration immediately before."
            self.phony = True
        else:
            self.phony = False
        self.dependencies = [d for d in match.group(4).split(" ") if d]
        self.command_string = match.group(6).strip()

    def relocate(self, directory):
        self.goals = os.path.join(directory, self.goals)
        self.dependencies = [os.path.join(directory, dep)
                             for dep in self.dependencies]
        self.command_string = "cd " + directory + " && " + self.command_string


class Makefile():
    def __init__(self, filename):
        self.filename = filename

    def goals(self):
        for match in Goal.goal_regex.finditer(open(self.filename).read()):
            yield Goal(match)


def process_sub_file(directory, target, extra_deps):
    whole = dict()

    def output_sub_target(target, extra_deps):
        goal = whole[target]
        if goal.phony:
            print(".PHONY :", goal.goals)
        print(goal.goals, ":", " ".join(goal.dependencies), extra_deps)
        if goal.command_string:
            print("\t" + goal.command_string)
        for dep in goal.dependencies:
            output_sub_target(dep, extra_deps)

    for goal in Makefile(os.path.join(directory, "makefile")).goals():
        goal.relocate(directory)
        whole[goal.goals] = goal
    output_sub_target(os.path.join(directory, target), extra_deps)

def process_top_file():
    for goal in Makefile("makefile").goals():
        if goal.phony:
            print(".PHONY :", goal.goals)

        if goal.command_string:
            command = goal.command_string
            command_match = re.match("cd ([^ \n]*) && make ([^ \n]*)", command)
            if command_match:
                directory = command_match.group(1)
                sub_goal = command_match.group(2)
                assert len(goal.goals.split(" ")) == 1, "Restriction: Only one goal"
                goal_with_deps = goal.goals + "_DEPS"
                # Output of a transformed goal
                print(".PHONY :", goal_with_deps)
                print(goal_with_deps, ":", " ".join(goal.dependencies))
                goal_for_sub = directory + "/" + sub_goal
                print(goal.goals, ":", goal_with_deps, goal_for_sub)
                process_sub_file(directory, sub_goal, goal_with_deps)
                continue
        # Output of a not transformed goal
        print(goal.goals, ":", " ".join(goal.dependencies))
        if goal.command_string:
            print("\t" + command)

def main():
    process_top_file()

main()
