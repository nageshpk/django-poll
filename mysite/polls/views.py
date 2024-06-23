from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
# from django.template import loader


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    # template = loader.get_template("polls/index.html")
    # return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)



def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return HttpResponse(f"You're looking at question {question_id}")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {'question': question})



def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {'question': question})
    # return HttpResponse(f"You're looking at results of the question {question_id}")




def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message": "You did not select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    # return HttpResponse(f"You are voting on question {question_id}")

