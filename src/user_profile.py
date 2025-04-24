from dataclasses import dataclass
from enum import Enum
from typing import Optional

class ActivityLevel(Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    VERY_ACTIVE = "very_active"

class DietaryPreference(Enum):
    NONE = "none"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    GLUTEN_FREE = "gluten_free"
    KETO = "keto"
    PALEO = "paleo"
    MEDITERRANEAN = "mediterranean"
    LOW_CARB = "low_carb"
    LOW_FAT = "low_fat"

class HealthGoal(Enum):
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"

class MealFrequency(Enum):
    THREE_MEALS = "three_meals"
    FIVE_MEALS = "five_meals"
    INTERMITTENT_FASTING = "intermittent_fasting"
    CUSTOM = "custom"

class FoodPreference(Enum):
    ANYTHING = "anything"
    PREFER_MEAT = "prefer_meat"
    PREFER_FISH = "prefer_fish"
    PREFER_VEGETABLES = "prefer_vegetables"
    PREFER_GRAINS = "prefer_grains"
    PREFER_DAIRY = "prefer_dairy"

class CookingSkill(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class UserProfile:
    age: int
    gender: str
    weight: float  # in kg
    height: float  # in cm
    activity_level: ActivityLevel
    dietary_preference: DietaryPreference
    health_goal: HealthGoal
    meal_frequency: MealFrequency = MealFrequency.THREE_MEALS
    food_preference: FoodPreference = FoodPreference.ANYTHING
    cooking_skill: CookingSkill = CookingSkill.INTERMEDIATE
    allergies: Optional[list[str]] = None
    preferred_cuisines: Optional[list[str]] = None
    disliked_foods: Optional[list[str]] = None
    meal_prep_time: Optional[int] = None  # in minutes

    def calculate_bmr(self) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if self.gender.lower() == "male":
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161

    def calculate_tdee(self) -> float:
        """Calculate Total Daily Energy Expenditure"""
        activity_multipliers = {
            ActivityLevel.SEDENTARY: 1.2,
            ActivityLevel.LIGHT: 1.375,
            ActivityLevel.MODERATE: 1.55,
            ActivityLevel.VERY_ACTIVE: 1.725
        }
        return self.calculate_bmr() * activity_multipliers[self.activity_level]

    def calculate_target_calories(self) -> float:
        """Calculate target calories based on health goal"""
        tdee = self.calculate_tdee()
        goal_adjustments = {
            HealthGoal.WEIGHT_LOSS: -500,  # Caloric deficit
            HealthGoal.MUSCLE_GAIN: 300,   # Caloric surplus
            HealthGoal.MAINTENANCE: 0      # Maintain current weight
        }
        return tdee + goal_adjustments[self.health_goal]

    def calculate_macros(self) -> dict:
        """Calculate recommended macronutrient distribution"""
        target_calories = self.calculate_target_calories()
        
        # Default macro ratios (protein/carbs/fats)
        macro_ratios = {
            HealthGoal.WEIGHT_LOSS: (0.40, 0.35, 0.25),
            HealthGoal.MUSCLE_GAIN: (0.30, 0.50, 0.20),
            HealthGoal.MAINTENANCE: (0.30, 0.40, 0.30)
        }
        
        protein_ratio, carb_ratio, fat_ratio = macro_ratios[self.health_goal]
        
        return {
            "protein": (target_calories * protein_ratio) / 4,  # 4 calories per gram of protein
            "carbs": (target_calories * carb_ratio) / 4,    # 4 calories per gram of carbs
            "fats": (target_calories * fat_ratio) / 9      # 9 calories per gram of fat
        }