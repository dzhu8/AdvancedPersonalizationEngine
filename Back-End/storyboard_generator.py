from typing import Dict, Any, Optional
import json

class StoryboardGenerator:
    @staticmethod
    def get_default_storyboard_prompt() -> str:
        return """Using the provided characteristics, create a detailed 10-second storyboard for a high-energy Coca-Cola advertisement tailored to this individual. The storyboard should be optimized for AI video generation software (e.g., Sora, Runway, Minimax, Luma) and include the following details:
Scene Breakdown – Provide a structured sequence of shots, ensuring smooth transitions and a compelling narrative arc.
Camera Movements – Specify shot types to enhance the cinematic feel.
Lighting & Mood – Define the lighting conditions and overall atmosphere.
Environmental Details – Include background elements that interact with the subject.
subject descrption: Describe the subject's appearence in each scene. Always describe the subject in each scene
Subject Actions & Expressions – Clearly describe movements, facial expressions, and interactions with Coca-Cola to evoke refreshment, excitement, and freedom.
Editing & Transitions – Indicate pacing to create dynamic storytelling.
Audio & Sound Design – Include ambient sounds, music choices, and key sound effects .
Color Palette & Visual Style – Describe the aesthetic using Coca-Cola's signature reds, deep ocean blues, and golden tones for an aspirational, lifestyle-focused look.
Text & Branding Elements – Ensure Coca-Cola branding, tagline placement, and product visibility are naturally integrated within the visuals. Instead of using the persons name, describe him briefly DO not use emojis
Describe the actions as easy as possible and as clear as possible
Each scene should start with the description what the subject looks like physically.
Exactly 4 scenes. The last one should be a display of the Coca-Cola logo.

Return the JSON object only, with each scene as a key."""

    @staticmethod
    def validate_storyboard_json(json_str: str) -> Dict[str, Any]:
        """Validate and parse the storyboard JSON"""
        try:
            data = json.loads(json_str)
            if not isinstance(data, dict):
                raise ValueError("Storyboard must be a JSON object")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}") 