import os

from azure.identity._credentials import ManagedIdentityCredential
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


def get_token():
    #   logging.info(f"Getting token for managed identity")
    # print('here', os.environ["IDENTITY_ENDPOINT"])
    #   pprint.pprint(list(os.environ.items()))
    default_credential = ManagedIdentityCredential()
#   default_credential = DefaultAzureCredential(managed_identity_client_id='dd3d6c47-2893-4054-ae9c-ef5a40aef484')
    token = default_credential.get_token(
        "https://ossrdbms-aad.database.windows.net/.default").token
#   logging.info(f"Token aquired")
    print(token)
    return token


class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    get_token()

    def get(self, request):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return render(request, "polls/index.html", {"drivers": get_token()})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    get_token()

    def get_queryset(self):
        """
        Update the model, excluding any questions that aren't published yet.
        """
        return [Question.objects.filter(pub_date__lte=timezone.now()), get_token()]


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
