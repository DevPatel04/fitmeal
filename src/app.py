import streamlit as st
from user_profile import UserProfile, ActivityLevel, DietaryPreference, HealthGoal, MealFrequency, FoodPreference, CookingSkill
from meal_planner import MealPlanner
from meal_planner import meal_order

# Set page config with custom theme
st.set_page_config(
    page_title="NutriPlan AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Card styling */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-size: 1.1em;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: #FFFFFF10;
        border-radius: 5px 5px 0px 0px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF20;
    }
    
    /* Input field styling */
    div.row-widget.stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label {
        background-color: #FFFFFF10;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 5px;
        text-align: center;
    }
    
    /* Card container */
    .css-12oz5g7.egzxvld2 {
        padding: 2rem;
        border-radius: 10px;
        background-color: #FFFFFF05;
    }
    
    /* Headers */
    h1, h2, h3 {
        margin-bottom: 1.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #FFFFFF10;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🥗 NutriPlan AI")
        st.write("Your personalized AI-powered meal planner")
    with col2:
        st.image("https://img.icons8.com/clouds/200/000000/healthy-food.png", width=100)

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["😊 Profile", "🍽️ Preferences", "✨ Generate Plan"])

    # Profile Tab
    with tab1:
        st.header("Let's Get to Know You")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.subheader("📋 Basic Information")
                age = st.number_input("Age", min_value=18, max_value=100, value=30)
                gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
                
                col_w, col_h = st.columns(2)
                with col_w:
                    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
                with col_h:
                    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
                    with st.expander("Height Converter (ft/in → cm)"):
                        feet = st.number_input("Feet", min_value=0, max_value=8, value=5, step=1)
                        inches = st.number_input("Inches", min_value=0, max_value=11, value=7, step=1)
                        if st.button("Convert to cm", key="convert_height"):
                            converted_cm = round((feet * 12 + inches) * 2.54, 1)
                            st.success(f"{feet} ft {inches} in = {converted_cm} cm")
        
        with col2:
            with st.container():
                st.subheader("🎯 Goals & Activity")
                activity = st.select_slider(
                    "Activity Level",
                    options=[level.value for level in ActivityLevel],
                    format_func=lambda x: x.replace('_', ' ').title()
                )
                
                goal = st.radio(
                    "What's your main health goal?",
                    [g.value for g in HealthGoal],
                    format_func=lambda x: x.replace('_', ' ').title(),
                    horizontal=True
                )

        # Add navigation message at the end of Profile tab
        st.markdown("---")
        st.info("✨ Great job completing your profile! Click on '🍽️ Preferences' tab to continue.")

    # Preferences Tab
    with tab2:
        st.header("Customize Your Meal Plan")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.subheader("🍳 Dietary Preferences")
                diet_pref = st.selectbox(
                    "Dietary Style",
                    [pref.value for pref in DietaryPreference],
                    format_func=lambda x: x.replace('_', ' ').title()
                )
                
                allergies = st.text_area(
                    "Any allergies or intolerances?",
                    placeholder="Enter allergies separated by commas..."
                )
                allergies = allergies.split(',') if allergies else None
                
                meal_freq = st.radio(
                    "Preferred Meal Schedule",
                    [freq.value for freq in MealFrequency],
                    format_func=lambda x: x.replace('_', ' ').title(),
                    horizontal=True
                )
        
        with col2:
            with st.container():
                st.subheader("👨‍🍳 Cooking Preferences")
                cooking_skill = st.select_slider(
                    "Cooking Expertise",
                    options=[skill.value for skill in CookingSkill],
                    format_func=lambda x: x.replace('_', ' ').title()
                )
                
                meal_prep_time = st.slider(
                    "Maximum prep time per meal (minutes)",
                    min_value=15,
                    max_value=120,
                    value=30,
                    step=15
                )
                
                food_pref = st.multiselect(
                    "Food Preferences",
                    [pref.value for pref in FoodPreference],
                    format_func=lambda x: x.replace('_', ' ').title()
                )
                
                cuisines = st.multiselect(
                    "Preferred Cuisines",
                    ["Italian", "Mexican", "Indian", "Chinese", "Japanese",
                     "Mediterranean", "American", "Thai", "Middle Eastern", "Other"]
                )
                
                disliked_foods = st.text_area(
                    "Foods you'd rather avoid",
                    placeholder="Enter foods separated by commas..."
                )
                disliked_foods = disliked_foods.split(',') if disliked_foods else None

        # Add navigation message at the end of Preferences tab
        st.markdown("---")
        st.info("✨ Perfect! Your preferences are set. Click on '✨ Generate Plan' tab to create your meal plan.")

    # Generate Plan Tab
    with tab3:
        st.header("Generate Your Meal Plan")
        
        # Summary cards before generation
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container():
                st.subheader("👤 Profile Summary")
                st.write(f"Age: {age} years")
                st.write(f"Gender: {gender}")
                st.write(f"Weight: {weight} kg")
                st.write(f"Height: {height} cm")
                st.write(f"Activity: {activity.replace('_', ' ').title()}")
        
        with col2:
            with st.container():
                st.subheader("🥗 Diet Summary")
                st.write(f"Diet: {diet_pref.replace('_', ' ').title()}")
                st.write(f"Goal: {goal.replace('_', ' ').title()}")
                st.write(f"Meals: {meal_freq.replace('_', ' ').title()}")
                if allergies:
                    st.write(f"Allergies: {', '.join(allergies)}")
        
        with col3:
            with st.container():
                st.subheader("👨‍🍳 Cooking Summary")
                st.write(f"Skill: {cooking_skill.replace('_', ' ').title()}")
                st.write(f"Prep Time: {meal_prep_time} minutes")
                if cuisines:
                    st.write(f"Cuisines: {', '.join(cuisines)}")

        # Add duration selector
        plan_duration = st.radio(
            "Select Plan Duration",
            ["Daily Plan", "Weekly Plan"],
            horizontal=True,
            help="Choose whether you want a meal plan for a single day or for the entire week"
        )

        generate_button = st.button("✨ Generate My Personalized Meal Plan", type="primary", use_container_width=True)

        if generate_button:
            try:
                # Create user profile
                user_profile = UserProfile(
                    age=age,
                    gender=gender,
                    weight=weight,
                    height=height,
                    activity_level=ActivityLevel(activity),
                    dietary_preference=DietaryPreference(diet_pref),
                    health_goal=HealthGoal(goal),
                    meal_frequency=MealFrequency(meal_freq),
                    food_preference=FoodPreference(food_pref[0] if food_pref else "anything"),
                    cooking_skill=CookingSkill(cooking_skill),
                    allergies=allergies,
                    preferred_cuisines=cuisines,
                    disliked_foods=disliked_foods,
                    meal_prep_time=meal_prep_time
                )

                # Generate meal plan with loading animation
                with st.spinner(f"🧙‍♂️ Creating your perfect {'weekly' if plan_duration == 'Weekly Plan' else 'daily'} meal plan... This might take a moment."):
                    meal_planner = MealPlanner()
                    if plan_duration == "Weekly Plan":
                        weekly_plan = meal_planner.generate_weekly_meal_plan(user_profile)
                        st.subheader("🗓️ Your Weekly Meal Plan")
                        
                        # Display each day's meals
                        for day_num, daily_plan in enumerate(weekly_plan.daily_plans, 1):
                            with st.expander(f"Day {day_num}"):
                                # Sort meals by time
                                sorted_meals = sorted(daily_plan.meals, 
                                                   key=lambda x: meal_order.get(x.meal_type.lower(), 99))

                                # Create meal cards in a grid
                                cols = st.columns(min(3, len(sorted_meals)))
                                for idx, meal in enumerate(sorted_meals):
                                    with cols[idx % 3]:
                                        with st.container():
                                            st.markdown(f"### {meal.meal_type.title()}")
                                            st.markdown(f"**{meal.name}**")

                                            st.markdown("#### 📝 Instructions")
                                            for i, step in enumerate(meal.instructions, 1):
                                                st.write(f"{i}. {step}")

                                            st.markdown("#### 🥗 Ingredients")
                                            for ingredient in meal.ingredients:
                                                st.write(f"• {ingredient}")

                                            st.markdown("#### 📊 Nutrition")
                                            nutrition_cols = st.columns(4)
                                            with nutrition_cols[0]:
                                                st.metric("Calories", f"{meal.nutrition['calories']:.0f}")
                                            with nutrition_cols[1]:
                                                st.metric("Protein", f"{meal.nutrition['protein']:.1f}g")
                                            with nutrition_cols[2]:
                                                st.metric("Carbs", f"{meal.nutrition['carbs']:.1f}g")
                                            with nutrition_cols[3]:
                                                st.metric("Fats", f"{meal.nutrition['fats']:.1f}g")
                                            st.info(f"⏱️ Prep Time: {meal.prep_time} minutes")
                    else:
                        daily_plan = meal_planner.generate_meal_plan(user_profile)
                        st.subheader("🍽️ Your Daily Meal Plan")
                        
                        # Sort meals by time
                        sorted_meals = sorted(daily_plan.meals, 
                                           key=lambda x: meal_order.get(x.meal_type.lower(), 99))

                        # Create meal cards in a grid
                        cols = st.columns(min(3, len(sorted_meals)))
                        for idx, meal in enumerate(sorted_meals):
                            with cols[idx % 3]:
                                with st.container():
                                    st.markdown(f"### {meal.meal_type.title()}")
                                    st.markdown(f"**{meal.name}**")
                                    
                                    with st.expander("View Details"):
                                        st.markdown("#### 📝 Instructions")
                                        for i, step in enumerate(meal.instructions, 1):
                                            st.write(f"{i}. {step}")
                                        
                                        st.markdown("#### 🥗 Ingredients")
                                        for ingredient in meal.ingredients:
                                            st.write(f"• {ingredient}")
                                        
                                        st.markdown("#### 📊 Nutrition")
                                        nutrition_cols = st.columns(4)
                                        with nutrition_cols[0]:
                                            st.metric("Calories", f"{meal.nutrition['calories']:.0f}")
                                        with nutrition_cols[1]:
                                            st.metric("Protein", f"{meal.nutrition['protein']:.1f}g")
                                        with nutrition_cols[2]:
                                            st.metric("Carbs", f"{meal.nutrition['carbs']:.1f}g")
                                        with nutrition_cols[3]:
                                            st.metric("Fats", f"{meal.nutrition['fats']:.1f}g")
                                        
                                        st.info(f"⏱️ Prep Time: {meal.prep_time} minutes")

                # Add completion message at the end of Generate Plan tab
                st.markdown("---")
                st.success(f"🎉 Your personalized {'weekly' if plan_duration == 'Weekly Plan' else 'daily'} meal plan is ready! Feel free to adjust your preferences and generate a new plan anytime.")

            except Exception as e:
                st.error(f"Oops! Something went wrong while creating your meal plan: {str(e)}")

if __name__ == "__main__":
    main()
