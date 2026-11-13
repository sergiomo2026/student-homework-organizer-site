
from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_title("Student Homework Organizer")

set_site_information(
    author="Sergio Morales",
    description="A website that helps students organize homework assignments, "
                "keep track of due dates, organize work by class, and track "
                "completed assignments.",
    sources="Drafter documentation and class materials.",
    planning=[],
    links=[]
)

hide_debug_information()
set_website_framed(False)


@dataclass
class Assignment:
    assignment_name: str
    class_name: str
    due_date: str
    is_completed: bool


@dataclass
class State:
    student_name: str
    assignments: list[Assignment]
    selected_class: str
    completed_count: int


@route
def index(state: State) -> Page:
    """Display the homepage of the homework organizer.

    Parameters:
        state: The current website information, including the student
            and their assignments.

    Returns:
        A Page displaying the welcome message and navigation buttons.

    Example:
        index(state) displays the homepage for the current student.
    """
    return Page(state, [
        Header("Student Homework Organizer"),
        "Welcome to your homework organizer, " + state.student_name + "!",
        "Use this website to keep track of your assignments.",
        Button("Add an Assignment", "add_assignment"),
        Button("About This Website", "about"),
        Button("View All Assignments", "all_assignments"),
        Button("Assignments by Class", "class_assignments"),
        Button("View Completed Work", "completed_work"),
        Button("Change Student Name", "change_name")
    ])


@route
def about(state: State) -> Page:
    """Explain the purpose of the homework organizer.

    Parameters:
        state: The current website information.

    Returns:
        A Page explaining the purpose and features of the website.

    Example:
        about(state) displays the About page.
    """
    return Page(state, [
        Header("About"),
        "This website helps students organize their homework.",
        "You can add assignments, choose classes, and track completed work.",
        Button("Home", "index")
    ])


@route
def add_assignment(state: State) -> Page:
    """Display the form for adding a homework assignment.

    Parameters:
        state: The current website information.

    Returns:
        A Page containing input fields for the assignment name,
        class, and due date.

    Example:
        add_assignment(state) displays the assignment form.
    """
    return Page(state, [
        Header("Add an Assignment"),
        "Assignment Name:",
        TextBox("assignment_name"),
        "Class:",
        SelectBox("class_name", [
            "CISC 106",
            "MATH",
            "CHEM",
            "ENGL",
            "Other"
        ]),
        "Due Date:",
        TextBox("due_date"),
        Button("Save Assignment", "save_assignment")
    ])


@route
def save_assignment(state: State, assignment_name: str,
                    class_name: str, due_date: str) -> Page:
    """Save a new assignment in the student's assignment list.

    Parameters:
        state: The current website information and assignment list.
        assignment_name: The name of the homework assignment.
        class_name: The class the assignment belongs to.
        due_date: The assignment's due date.

    Returns:
        A Page displaying the homepage after saving the assignment.

    Example:
        save_assignment(state, "Homework 1", "CISC 106", "11/20")
        adds a new CISC 106 assignment due on 11/20.
    """
    if assignment_name != "":
        new_assignment = Assignment(
            assignment_name,
            class_name,
            due_date,
            False
        )
        state.assignments.append(new_assignment)
        state.selected_class = class_name

    return index(state)


@route
def all_assignments(state: State) -> Page:
    """Display all saved homework assignments.

    Parameters:
        state: The current website information and assignment list.

    Returns:
        A Page displaying all assignments with options to complete
        or delete them.

    Example:
        all_assignments(state) displays every saved assignment.
    """
    assignment_list = [
        Header("All Assignments")
    ]

    if len(state.assignments) == 0:
        assignment_list.append("You have no assignments yet.")

    assignment_number = 0

    for assignment in state.assignments:
        assignment_list.append(
            assignment.assignment_name + " - " +
            assignment.class_name + " - Due: " +
            assignment.due_date
        )

        assignment_list.append(
            Button(
                "Delete Assignment",
                "delete_assignment",
                [Argument("assignment_index", assignment_number)]
            )
        )

        if assignment.is_completed:
            assignment_list.append("Status: Completed")
        else:
            assignment_list.append("Status: Not Completed")
            assignment_list.append(
                Button(
                    "Mark as Completed",
                    "complete_assignment",
                    [Argument("assignment_index", assignment_number)]
                )
            )

        assignment_number = assignment_number + 1

    assignment_list.append(Button("Home", "index"))

    return Page(state, assignment_list)


@route
def complete_assignment(state: State, assignment_index: int) -> Page:
    """Mark an assignment as completed and update the completed count.

    Parameters:
        state: The current website information and assignment list.
        assignment_index: The position of the assignment in the list.

    Returns:
        A Page displaying the updated assignment list.

    Example:
        complete_assignment(state, 0) marks the first assignment
        as completed.
    """
    if assignment_index >= 0 and assignment_index < len(state.assignments):
        if not state.assignments[assignment_index].is_completed:
            state.assignments[assignment_index].is_completed = True
            state.completed_count = state.completed_count + 1

    return all_assignments(state)


@route
def delete_assignment(state: State, assignment_index: int) -> Page:
    """Delete an assignment from the student's assignment list.

    Parameters:
        state: The current website information and assignment list.
        assignment_index: The position of the assignment to delete.

    Returns:
        A Page displaying the updated assignment list.

    Example:
        delete_assignment(state, 0) deletes the first assignment.
    """
    if assignment_index >= 0 and assignment_index < len(state.assignments):
        if state.assignments[assignment_index].is_completed:
            state.completed_count = state.completed_count - 1

        del state.assignments[assignment_index]

    return all_assignments(state)


@route
def class_assignments(state: State, class_name: str = "") -> Page:
    """Display a form for choosing a class to view assignments.

    Parameters:
        state: The current website information.
        class_name: The selected class, if one is provided.

    Returns:
        A Page containing a class selection menu.

    Example:
        class_assignments(state) displays the class selection page.
    """
    return Page(state, [
        Header("Assignments by Class"),
        "Choose a class:",
        SelectBox("class_name", [
            "CISC 106",
            "MATH",
            "CHEM",
            "ENGL",
            "Other"
        ]),
        Button("Find Assignments", "show_class_assignments"),
        Button("Home", "index")
    ])


@route
def show_class_assignments(state: State, class_name: str) -> Page:
    """Display assignments that belong to the selected class.

    Parameters:
        state: The current website information and assignment list.
        class_name: The name of the class whose assignments are displayed.

    Returns:
        A Page displaying assignments for the selected class.

    Example:
        show_class_assignments(state, "CISC 106") displays
        CISC 106 assignments.
    """
    assignment_list = [
        Header("Assignments for " + class_name)
    ]

    state.selected_class = class_name
    found_assignment = False

    for assignment in state.assignments:
        if assignment.class_name == class_name:
            found_assignment = True
            assignment_list.append(
                assignment.assignment_name + " - Due: " +
                assignment.due_date
            )

    if not found_assignment:
        assignment_list.append("No assignments found for this class.")

    assignment_list.append(Button("Home", "index"))
    assignment_list.append(Button("All Assignments", "all_assignments"))

    return Page(state, assignment_list)


@route
def completed_work(state: State) -> Page:
    """Display all assignments that the student has completed.

    Parameters:
        state: The current website information and assignment list.

    Returns:
        A Page displaying completed assignments and the completed count.

    Example:
        completed_work(state) displays the student's completed assignments.
    """
    assignment_list = [
        Header("Completed Work")
    ]

    found_assignment = False

    for assignment in state.assignments:
        if assignment.is_completed:
            found_assignment = True
            assignment_list.append(
                assignment.assignment_name + " - " +
                assignment.class_name + " - Due: " +
                assignment.due_date
            )

    if not found_assignment:
        assignment_list.append("You have no completed assignments yet.")

    assignment_list.append(
        "Total Completed: " + str(state.completed_count)
    )
    assignment_list.append(Button("Home", "index"))
    assignment_list.append(Button("All Assignments", "all_assignments"))

    return Page(state, assignment_list)


@route
def change_name(state: State) -> Page:
    """Display a form for changing the student's name.

    Parameters:
        state: The current website information.

    Returns:
        A Page containing a text box for entering a new student name.

    Example:
        change_name(state) displays the name-changing form.
    """
    return Page(state, [
        Header("Change Student Name"),
        "Enter your name:",
        TextBox("student_name"),
        Button("Save Name", "save_name"),
        Button("Home", "index")
    ])


@route
def save_name(state: State, student_name: str) -> Page:
    """Save the student's new name.

    Parameters:
        state: The current website information.
        student_name: The new name entered by the student.

    Returns:
        A Page displaying the homepage with the updated student name.

    Example:
        save_name(state, "Alex") changes the student's name to Alex.
    """
    if student_name != "":
        state.student_name = student_name

    return index(state)


# Test adding an assignment
test_state = State("Test Student", [], "CISC 106", 0)

save_assignment(test_state, "Homework 1", "CISC 106", "11/20")
assert_equal(len(test_state.assignments), 1)
assert_equal(test_state.selected_class, "CISC 106")

# Test completing an assignment
complete_assignment(test_state, 0)
assert_equal(test_state.assignments[0].is_completed, True)
assert_equal(test_state.completed_count, 1)

# Test deleting a completed assignment
delete_assignment(test_state, 0)
assert_equal(len(test_state.assignments), 0)
assert_equal(test_state.completed_count, 0)

# Test changing the student's name
save_name(test_state, "Alex")
assert_equal(test_state.student_name, "Alex")

# Test deleting an incomplete assignment
save_assignment(test_state, "Homework 2", "MATH", "11/22")
delete_assignment(test_state, 0)
assert_equal(len(test_state.assignments), 0)
assert_equal(test_state.completed_count, 0)


start_server(State("Student", [], "CISC 106", 0))
