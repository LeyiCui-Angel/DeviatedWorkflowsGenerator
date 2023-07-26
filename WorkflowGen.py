import itertools
from itertools import combinations,combinations_with_replacement

# input: initial workflow
# input format: select patient A; click <A>; Click <B>; choose Starting Date; click <Save>
iniWorkflow = input("Enter the initial workflow: ").split(";")
# input: error type
# supported error types: omission/repetition/permutation(commission?)
errType = input("Choose an error type (omission/repetition/permutation): ").lower()
# input: level of erroneous actions generated
# select 0 to not include any
level = int(input("Choose the level of erroneous actions generated: "))

# omission
def omission(actions, level):
    if level == 0:
        return [actions]

    omissions = []
    numActions = len(actions)

    for i in range(1, level + 1):
        omittedCombo = combinations(range(numActions), i)
        for omitted in omittedCombo:
            deviatedWorkflow = [actions[j] for j in range(numActions) if j not in omitted]
            omissions.append(deviatedWorkflow)

    return omissions

# repetition
def repetition(actions, level):
    repetitions = [actions]
    workflowSet = {tuple(actions)}  # set for checking duplicates

    for l in range(1, level+1):
        new_workflows = []
        for workflow in repetitions:
            for i in range(len(workflow)):
                new_workflow = workflow[:i+1] + [workflow[i]] + workflow[i+1:]
                new_workflow_tuple = tuple(new_workflow)
                # Only add new_workflow to new_workflows if it's not a duplicate
                if new_workflow_tuple not in workflowSet:
                    new_workflows.append(new_workflow)
                    workflowSet.add(new_workflow_tuple)
        repetitions += new_workflows

    return repetitions

# permutation
def permutation(actions, level):
    # If level = 0, return the original workflow
    if level == 0:
        return [actions]

    permutations = [actions]

    # If level > 0, generate permutations
    for l in range(1, level + 1):
        for perm in itertools.permutations(actions, l + 1):
            new_perm = actions.copy()

            # put the permuted actions back in their original places
            indices = sorted([actions.index(act) for act in perm])
            for i, act in zip(indices, perm):
                new_perm[i] = act

            if new_perm not in permutations:
                permutations.append(new_perm)

    return permutations

if errType=="omission":
    r = omission(iniWorkflow, level)
    print(r)
elif errType=="repetition":
    r = repetition(iniWorkflow, level)
    print(r)
elif errType=="permutation":
    r = permutation(iniWorkflow, level)
    print(r)
else:
    print("Please make sure that you entered a correct error type.")