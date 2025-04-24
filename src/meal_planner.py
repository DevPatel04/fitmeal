from typing import List, Dict
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

from user_profile import UserProfile, DietaryPreference, MealFrequency

meal_order = {
    "breakfast": 0,
    "morning snack": 1,
    "lunch": 2,
    "afternoon snack": 3,
    "dinner": 4,
    "first meal": 0,
    "second meal": 1,
    "final meal": 2,
    "early morning meal": 0,
    "mid-morning meal": 1,
    "midday meal": 2,
    "afternoon meal": 3,
    "evening meal": 4
}

class Meal(BaseModel):
    name: str = Field(description="Name of the meal")
    meal_type: str = Field(description="Type of meal (e.g., breakfast, lunch, dinner, morning snack, afternoon snack)")
    ingredients: List[str] = Field(description="List of ingredients needed")
    instructions: List[str] = Field(description="Step by step cooking instructions")
    nutrition: Dict[str, float] = Field(description="Nutritional information including calories, protein, carbs, and fats")
    prep_time: int = Field(description="Estimated preparation time in minutes")

class DailyMealPlan(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snacks: List[Meal] = Field(default_factory=list)

    def __init__(self, **data):
        # Convert meals list to specific meal types
        if 'meals' in data:
            meals = data.pop('meals')
            # Sort meals based on meal_order
            sorted_meals = sorted(meals, key=lambda x: meal_order.get(x['meal_type'].lower(), 999))
            
            # Process meals in the correct order
            for meal in sorted_meals:
                meal_type = meal['meal_type'].lower()
                if meal_type in ['breakfast', 'first meal', 'early morning meal']:
                    data['breakfast'] = Meal(**meal)
                elif meal_type in ['lunch', 'second meal', 'midday meal']:
                    data['lunch'] = Meal(**meal)
                elif meal_type in ['dinner', 'final meal', 'evening meal']:
                    data['dinner'] = Meal(**meal)
                else:
                    if 'snacks' not in data:
                        data['snacks'] = []
                    data['snacks'].append(Meal(**meal))
        super().__init__(**data)

    @property
    def meals(self) -> List[Meal]:
        """Return all meals for the day including snacks"""
        return [self.breakfast, self.lunch, self.dinner] + self.snacks
    total_calories: float = Field(description="Total calories for all meals")
    total_protein: float = Field(description="Total protein in grams")
    total_carbs: float = Field(description="Total carbs in grams")
    total_fats: float = Field(description="Total fats in grams")

class WeeklyMealPlan(BaseModel):
    daily_plans: List[DailyMealPlan] = Field(description="List of daily meal plans for the week")

class MealPlanner:
    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.llm = ChatGroq(api_key=self.groq_api_key,
        model = "llama-3.3-70b-versatile",
        temperature = 0.5)
        self.daily_plan_parser = PydanticOutputParser(pydantic_object=DailyMealPlan)
        self.weekly_plan_parser = PydanticOutputParser(pydantic_object=WeeklyMealPlan)

    def _get_meal_structure(self, meal_frequency: MealFrequency) -> str:
        meal_structures = {
            MealFrequency.THREE_MEALS: """
                - Breakfast (morning)
                - Lunch (midday)
                - Dinner (evening)""",
            MealFrequency.FIVE_MEALS: """
                - Breakfast (early morning)
                - Morning Snack (mid-morning)
                - Lunch (midday)
                - Afternoon Snack (mid-afternoon)
                - Dinner (evening)""",
            MealFrequency.INTERMITTENT_FASTING: """
                For 16/8 Intermittent Fasting schedule (16 hours fasting, 8 hours eating window):
                - First Meal (12:00 PM - Breaking fast)
                - Second Meal (3:00 PM - Midday meal)
                - Final Meal (7:00 PM - Last meal before fasting)
                
                Note: Meals should be substantial and nutrient-dense to meet daily requirements within the eating window.""",
            MealFrequency.CUSTOM: """
                - Early Morning Meal
                - Mid-Morning Meal
                - Midday Meal
                - Afternoon Meal
                - Evening Meal"""
        }
        return meal_structures.get(meal_frequency, meal_structures[MealFrequency.THREE_MEALS])

    def _create_meal_plan_prompt(self, user_profile: UserProfile) -> str:
        meal_structure = self._get_meal_structure(user_profile.meal_frequency)
        
        base_prompt = f"""You are a professional nutritionist and meal planner. Create a daily meal plan that meets the following requirements:
            - Matches the user's dietary preferences and restrictions
            - Meets caloric and macronutrient targets
            - Includes healthy, balanced meals
            - Provides variety and is practical to prepare
            - Considers the user's cooking skill level and available prep time
            - Follows this specific meal structure:{meal_structure}
            - Incorporates preferred cuisines and avoids disliked foods"""

        if user_profile.meal_frequency == MealFrequency.INTERMITTENT_FASTING:
            base_prompt += """
            
            For Intermittent Fasting:
            - Design exactly 3 substantial meals within the 8-hour eating window
            - First meal should break the fast and be easily digestible
            - Space meals ~3 hours apart
            - Ensure each meal is nutrient-dense and satisfying
            - Include protein in each meal to maintain satiety
            - Consider adding healthy fats for sustained energy
            - Include complex carbs for sustained energy
            - Ensure the last meal is substantial enough to sustain through the fasting period"""
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", base_prompt),
            ("user", """Please create a daily meal plan for a user with the following profile:
            - Dietary preference: {dietary_preference}
            - Meal frequency: {meal_frequency}
            - Food preferences: {food_preference}
            - Cooking skill level: {cooking_skill}
            - Available meal prep time: {meal_prep_time} minutes
            - Preferred cuisines: {preferred_cuisines}
            - Disliked foods: {disliked_foods}
            - Daily calorie target: {target_calories}
            - Protein target: {protein_target}g
            - Carbs target: {carbs_target}g
            - Fats target: {fats_target}g
            - Any allergies: {allergies}
            
            Format the response as a JSON object with:
            - meals: list of meal objects, each containing:
              - name: string
              - meal_type: string (e.g., "First Meal", "Second Meal", "Final Meal" for IF)
              - ingredients: list of strings
              - instructions: list of strings (each string being one step)
              - nutrition: object with calories, protein, carbs, and fats as numbers
              - prep_time: number (in minutes)
            - total_calories: number
            - total_protein: number
            - total_carbs: number
            - total_fats: number""")
        ])

        macros = user_profile.calculate_macros()
        allergies = user_profile.allergies if user_profile.allergies else "None"
        disliked_foods = user_profile.disliked_foods if user_profile.disliked_foods else "None"
        preferred_cuisines = user_profile.preferred_cuisines if user_profile.preferred_cuisines else "No specific preferences"

        return prompt_template.format_messages(
            dietary_preference=user_profile.dietary_preference.value,
            meal_frequency=user_profile.meal_frequency.value,
            food_preference=user_profile.food_preference.value,
            cooking_skill=user_profile.cooking_skill.value,
            meal_prep_time=user_profile.meal_prep_time,
            preferred_cuisines=preferred_cuisines,
            disliked_foods=disliked_foods,
            target_calories=user_profile.calculate_target_calories(),
            protein_target=macros['protein'],
            carbs_target=macros['carbs'],
            fats_target=macros['fats'],
            allergies=allergies
        )

    def generate_meal_plan(self, user_profile: UserProfile) -> DailyMealPlan:
        """Generate a daily meal plan based on user profile and preferences"""
        prompt = self._create_meal_plan_prompt(user_profile)
        response = self.llm.invoke(prompt)
        
        try:
            # Ensure we're working with the content string
            if isinstance(response, tuple):
                response_content = response[0].content if hasattr(response[0], 'content') else str(response[0])
            else:
                response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Parse the response
            parsed_plan = self.daily_plan_parser.parse(response_content)
            
            # Validate the parsed plan
            if not isinstance(parsed_plan, DailyMealPlan):
                raise ValueError("Failed to parse response into DailyMealPlan")
            
            return parsed_plan
        except Exception as e:
            raise ValueError(f"Failed to generate meal plan: {str(e)}")

    def generate_weekly_meal_plan(self, user_profile: UserProfile) -> WeeklyMealPlan:
        """Generate a weekly meal plan based on user profile and preferences"""
        try:
            weekly_plan = []
            for day in range(7):  # Generate 7 days of meal plans
                try:
                    daily_plan = self.generate_meal_plan(user_profile)
                    if not isinstance(daily_plan, DailyMealPlan):
                        raise ValueError(f"Invalid daily meal plan generated for day {day + 1}")
                    weekly_plan.append(daily_plan)
                except Exception as e:
                    raise ValueError(f"Error generating plan for day {day + 1}: {str(e)}")
            
            if not weekly_plan:
                raise ValueError("No valid daily plans were generated")
            
            return WeeklyMealPlan(daily_plans=weekly_plan)
        except Exception as e:
            raise ValueError(f"Failed to generate weekly meal plan: {str(e)}")

# Define meal order for sorting at the top of the file, before the classes
