from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Scenario
from .gemini_client import ConversationAI
from django.views.decorators.http import require_POST


def start_chat(request, scenario_id):
    scenario = get_object_or_404(Scenario, id=scenario_id)
    user_level = request.GET.get("level", "beginner")
    request.session["user_level"] = user_level

    history_key = f"history_{scenario_id}"
    request.session[history_key] = []

    # Check if this scenario requires AI to start or user to start
    # For most scenarios (cafe, hotel), AI greets first
    # For some scenarios (directions), let user start
    
    user_starts_scenarios = ['asking for directions', 'directions']  # Add scenario names where user should start
    
    if scenario.name.lower() in [s.lower() for s in user_starts_scenarios]:
        # User starts - no AI message yet
        ai_message = None
        request.session[history_key] = []
    else:
        # AI starts with greeting
        ai = ConversationAI()
        ai_message = ai.start_conversation(scenario, user_level)["roleplay_response"]
        request.session[history_key] = [{"role": "ai", "content": ai_message}]

    vocab = getattr(scenario, "vocab", None) if user_level == "beginner" else None

    return render(request, "conversation/chat.html", {
        "scenario": scenario,
        "conversation_history": request.session[history_key],
        "vocab": vocab,
        "user_level": user_level,
    })


@csrf_exempt
def continue_chat(request, scenario_id):
    scenario = get_object_or_404(Scenario, id=scenario_id)
    user_level = request.POST.get("level") or request.session.get("user_level", "beginner")
    vocab = getattr(scenario, "vocab", None) if user_level == "beginner" else None

    history_key = f"history_{scenario_id}"
    conversation_history = request.session.get(history_key, [])

    if request.method == "POST":
        user_message = request.POST.get("user_message", "")
        if not user_message:
            return HttpResponseBadRequest("No message provided")

        conversation_history.append({"role": "user", "content": user_message})
        ai = ConversationAI()
        result = ai.continue_conversation(scenario, conversation_history, user_message, user_level)
        
        print("DEBUG - AI Result:", result)  # ← Add this to see what comes back
        
        ai_response = result["roleplay_response"]
        feedback = result.get("feedback", "") or result.get("language_feedback", "")  # Try both keys
        
        print("DEBUG - Feedback:", feedback)  # ← Add this too
        
        conversation_history.append({"role": "ai", "content": ai_response})
        request.session[history_key] = conversation_history
        
        return render(request, "conversation/chat.html", {
            "scenario": scenario,
            "user_level": user_level,
            "conversation_history": conversation_history,
            "vocab": vocab,
            "feedback": feedback,
        })
    
    # GET request
    return render(request, "conversation/chat.html", {
        "scenario": scenario,
        "user_level": user_level,
        "conversation_history": conversation_history,
        "vocab": vocab,
    })


def end_chat(request, scenario_id):
    scenario = get_object_or_404(Scenario, id=scenario_id)
    user_level = request.session.get("user_level", "beginner")
    history_key = f"history_{scenario_id}"
    conversation_history = request.session.get(history_key, [])
    user_messages = [msg for msg in conversation_history if msg["role"] == "user"]
    num_exchanges = len(user_messages)

    ai = ConversationAI()
    assessment = ai.generate_assessment(scenario=scenario, conversation_history=conversation_history, user_level=user_level)

    request.session[history_key] = []

    return render(request, "conversation/assessment.html", {
        "scenario": scenario,
        "user_level": user_level,
        "num_exchanges": num_exchanges,
        "assessment": assessment,
        "conversation_history": conversation_history,
    })


def index(request):
    scenarios = Scenario.objects.all()
    return render (request, 'conversation/index.html', {'scenarios': scenarios})
    
def phrase_practice(request):
    """List all scenarios for phrase practice"""
    scenarios = Scenario.objects.all()
    return render(request, 'conversation/phrase_practice.html', {
        'scenarios': scenarios
    })
def phrase_practice_scenario(request, scenario_id):
    """Show vocab builder for a specific scenario"""
    scenario = get_object_or_404(Scenario, id=scenario_id)
    
    return render(request, 'conversation/phrase_practice_simple.html', {
        'scenario': scenario,
        'vocab': scenario.vocab,
    })

def select_level_and_scenario(request):
    scenarios = Scenario.objects.all()
    
    if request.method == "POST":
        user_level = request.POST.get("user_level")
        scenario_id = request.POST.get("scenario_id")
        
        request.session['user_level'] = user_level
        request.session['scenario_id'] = scenario_id
        
        return redirect('continue_chat', scenario_id=scenario_id)
    
    return render(request, 'conversation/select_level_and_scenario.html', {
        'scenarios': scenarios,
    })

@require_POST
def end_conversation(request, scenario_id):
    request.session.pop("conversation_history", None)
    request.session.pop("feedback", None)
    # Optional: mark conversation complete in DB
    return redirect("select_level_and_scenario")
