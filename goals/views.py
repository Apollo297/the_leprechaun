from django.shortcuts import render


from goals.forms import GoalForm


def newgoal(request):
    form = GoalForm()
    template = 'capital_and_goals/new_goal.html'
    context = {'form': form}
    return render(request, template, context)
