from django.shortcuts import render, redirect
from .models import TestTopic, Question, Answer
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('select_topic')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('select_topic')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def select_topic(request):
    topics = TestTopic.objects.all()
    return render(request, 'select_topic.html', {'topics': topics})

@login_required
def start_test(request, topic_id):
    topic = TestTopic.objects.get(pk=topic_id)
    questions = topic.questions.all()
    request.session['questions'] = [question.id for question in questions]
    request.session['current_question'] = 0
    request.session['score'] = 0
    return redirect('show_question')

@login_required
def show_question(request):
    question_id = request.session.get('questions')[request.session.get('current_question')]
    question = Question.objects.get(pk=question_id)
    answers = question.answers.all()
    return render(request, 'show_question.html', {'question': question, 'answers': answers})
@login_required
def handle_answer(request):
    question_id = request.session.get('questions')[request.session.get('current_question')]
    question = Question.objects.get(pk=question_id)
    selected_answer_id = request.POST.get('answer')
    selected_answer = Answer.objects.get(pk=selected_answer_id)
    if selected_answer.is_correct:
        request.session['score'] += 1
    request.session['current_question'] += 1
    if request.session['current_question'] < len(request.session['questions']):
        return redirect('show_question')
    else:
        return redirect('show_result')
@login_required
def show_result(request):
    score = request.session['score']
    total_questions = len(request.session['questions'])
    percent_correct = (score / total_questions) * 100 if total_questions > 0 else 0
    percent_correct = round(percent_correct, 2)
    del request.session['questions']
    del request.session['current_question']
    del request.session['score']
    return render(request, 'show_result.html', {'score': score, 'total_questions': total_questions, 'percent_correct': percent_correct})
