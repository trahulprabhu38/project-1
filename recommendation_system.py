from sentence_transformers import SentenceTransformer, util
import json
import torch
import random
import pandas as pd

# ----------------------------
# Load the corpus
# ----------------------------

data={
    "Generalized Anxiety Disorder - Excessive Worry": "Identify your worry triggers and practice relaxation techniques like deep breathing or progressive muscle relaxation.",
    "Social Anxiety Disorder - Fear of Social Situations": "Gradually expose yourself to social situations and practice positive self-talk. Remember it's okay to feel nervous.",
    "Panic Disorder - Sudden Attacks of Fear": "Learn to recognize the symptoms of a panic attack and remind yourself that it will pass. Focus on your breathing.",
    "Major Depressive Disorder - Persistent Sadness": "Engage in small, achievable activities to boost your mood. Reach out to friends, family, or a mental health professional for support.",
    "Persistent Depressive Disorder (Dysthymia) - Long-Term Low Mood": "Establish a consistent daily routine and focus on self-care activities. Therapy can be very helpful for managing persistent low mood.",
    "Bipolar I Disorder - Mania and Depression": "Work closely with a psychiatrist to manage mood swings through medication and therapy. Develop a mood tracking system.",
    "Bipolar II Disorder - Hypomania and Depression": "Learn to recognize the signs of hypomania and depression early on. Maintain a consistent sleep schedule.",
    "Cyclothymic Disorder - Mild Mood Swings": "Practice mindfulness to increase awareness of your mood shifts. Therapy can help develop coping strategies.",
    "Obsessive-Compulsive Disorder (OCD) - Intrusive Thoughts and Compulsions": "Learn to manage intrusive thoughts without engaging in compulsions. Exposure and Response Prevention (ERP) therapy is effective.",
    "Body Dysmorphic Disorder - Preoccupation with Appearance": "Challenge negative thoughts about your appearance and focus on your inner qualities. Cognitive Behavioral Therapy (CBT) can be beneficial.",
    "Hoarding Disorder - Difficulty Discarding Possessions": "Seek professional help to develop strategies for decluttering and addressing the underlying emotional attachments.",
    "Trichotillomania (Hair-Pulling Disorder)": "Identify triggers for hair-pulling and develop competing responses with the guidance of a therapist.",
    "Excoriation (Skin-Picking) Disorder)": "Identify triggers for skin-picking and develop strategies to redirect these urges with the support of a therapist.",
    "Post-Traumatic Stress Disorder (PTSD) - Trauma Re-experiencing": "Practice grounding techniques to stay present. Seek therapy specifically designed for trauma, like EMDR or Trauma-Focused CBT.",
    "Acute Stress Disorder - Short-Term Trauma Symptoms": "Focus on self-care and seek support from friends, family, or a therapist in the immediate aftermath of a traumatic event.",
    "Adjustment Disorder - Difficulty Coping with Change": "Allow yourself time to adjust to the new situation and seek support to process your feelings.",
    "Schizophrenia - Hallucinations and Delusions": "Work closely with a psychiatrist for medication management and therapy to manage psychotic symptoms.",
    "Schizoaffective Disorder - Mood and Psychotic Symptoms": "Maintain consistent communication with your treatment team to manage both mood and psychotic symptoms effectively.",
    "Schizophreniform Disorder - Short-Term Psychotic Symptoms": "Seek early intervention and treatment to manage symptoms and prevent potential progression.",
    "Delusional Disorder - Fixed False Beliefs": "Engage in open and honest communication with a mental health professional to explore your beliefs.",
    "Brief Psychotic Disorder - Sudden Onset of Psychotic Symptoms": "Seek immediate professional help to manage acute symptoms and determine the underlying cause.",
    "Attention-Deficit/Hyperactivity Disorder (ADHD) - Inattention": "Use organizational tools like planners and reminders. Break down tasks into smaller steps.",
    "Attention-Deficit/Hyperactivity Disorder (ADHD) - Hyperactivity and Impulsivity": "Find healthy outlets for excess energy and practice strategies to manage impulsive behaviors.",
    "Autism Spectrum Disorder - Social Communication Challenges": "Develop social skills through practice and support. Create structured routines and predictable environments.",
    "Social Communication Disorder - Difficulty with Social Language": "Work with a speech-language therapist to improve understanding and use of social communication cues.",
    "Oppositional Defiant Disorder (ODD) - Defiant Behavior": "Focus on positive reinforcement and consistent boundaries. Therapy for both the individual and family can be helpful.",
    "Conduct Disorder - Violating Rules and Rights of Others": "Seek comprehensive therapy that addresses underlying issues and promotes prosocial behavior.",
    "Intellectual Disability - Limitations in Cognitive Functioning": "Focus on individual strengths and provide support tailored to specific needs and abilities.",
    "Specific Learning Disorder (e.g., Dyslexia) - Difficulty with Learning": "Seek educational support and accommodations tailored to the specific learning difficulty.",
    "Anorexia Nervosa - Restriction of Food Intake": "Seek comprehensive treatment involving medical, nutritional, and psychological support to address the eating disorder and underlying issues.",
    "Bulimia Nervosa - Binge Eating and Compensatory Behaviors": "Engage in therapy, such as CBT, to address unhealthy eating patterns and emotional regulation.",
    "Binge Eating Disorder - Recurrent Episodes of Binge Eating": "Seek therapy to address the triggers for binge eating and develop healthier coping mechanisms.",
    "Avoidant/Restrictive Food Intake Disorder (ARFID) - Selective Eating": "Work with a multidisciplinary team to gradually expand food intake and address any underlying anxieties.",
    "Substance Use Disorder - Dependence on Substances": "Seek professional help for detoxification and rehabilitation. Therapy and support groups are crucial for long-term recovery.",
    "Gambling Disorder - Compulsive Gambling Behavior": "Seek therapy and support groups like Gamblers Anonymous to address the urge to gamble and develop coping strategies.",
    "Internet Addiction - Excessive and Problematic Internet Use": "Set limits on internet use and find alternative activities. Therapy can help address underlying issues.",
    "Intermittent Explosive Disorder - Episodes of Intense Anger": "Learn to identify anger triggers and develop healthy coping mechanisms for managing anger.",
    "Kleptomania - Urge to Steal": "Seek therapy to understand the underlying reasons for stealing and develop strategies to manage urges.",
    "Pyromania - Urge to Set Fires": "Seek specialized therapy to address the fascination with fire and develop impulse control.",
    "Reactive Attachment Disorder - Difficulty Forming Attachments": "Provide a stable and nurturing environment. Therapy focused on building trust and attachment is essential.",
    "Disinhibited Social Engagement Disorder - Indiscriminate Sociability": "Provide consistent boundaries and teach appropriate social interactions. Therapy can help address underlying attachment issues.",
    "Personality Disorders (General) - Inflexible Personality Traits": "Long-term therapy, such as Dialectical Behavior Therapy (DBT) or Transference-Focused Psychotherapy (TFP), can help manage maladaptive patterns.",
    "Borderline Personality Disorder - Emotional Instability": "Dialectical Behavior Therapy (DBT) is a highly effective treatment for managing intense emotions and improving relationships.",
    "Narcissistic Personality Disorder - Grandiosity and Lack of Empathy": "Therapy can help develop self-awareness and improve interpersonal relationships.",
    "Antisocial Personality Disorder - Disregard for Others' Rights": "Treatment is often challenging but may involve therapy focused on managing impulsive behavior and developing empathy.",
    "Histrionic Personality Disorder - Excessive Emotionality and Attention Seeking": "Therapy can help develop a more stable sense of self and healthier ways of relating to others.",
    "Avoidant Personality Disorder - Social Inhibition and Fear of Rejection": "Therapy can help build self-esteem and gradually increase social engagement.",
    "Dependent Personality Disorder - Need to Be Taken Care Of": "Therapy focuses on developing autonomy and assertiveness.",
    "Obsessive-Compulsive Personality Disorder - Preoccupation with Orderliness": "Therapy can help develop flexibility and a more balanced perspective.",
    "Paranoid Personality Disorder - Suspiciousness and Mistrust": "Therapy aims to build trust and challenge paranoid thoughts.",
    "Schizoid Personality Disorder - Detachment from Social Relationships": "Therapy can help explore the desire for connection and develop social skills at the individual's pace.",
    "Schizotypal Personality Disorder - Eccentric Behavior and Thought Patterns": "Therapy can help manage unusual thoughts and behaviors and improve social interactions.",
    "Grief and Bereavement - Loss of a Loved One": "Allow yourself to grieve and seek support from friends, family, or a grief counselor.",
    "Relationship Problems - Communication Issues": "Practice active listening and assertive communication skills. Couples therapy can be beneficial.",
    "Low Self-Esteem - Negative Self-Image": "Challenge negative self-talk and focus on your strengths. Practice self-compassion.",
    "Stress Management - Feeling Overwhelmed": "Identify your stressors and develop healthy coping mechanisms like exercise, mindfulness, or hobbies.",
    "Burnout - Emotional and Physical Exhaustion": "Prioritize self-care and set boundaries between work and personal life.",
    "Compassion Fatigue - Emotional Toll of Helping Others": "Practice self-care and seek support from colleagues or supervisors.",
    "Vicarious Trauma - Secondary Exposure to Trauma": "Seek support and processing techniques specifically designed for vicarious trauma.",
    "Loneliness and Social Isolation - Lack of Connection": "Make an effort to connect with others and engage in social activities.",
    "Existential Crisis - Questioning Meaning and Purpose": "Explore your values and beliefs. Therapy or philosophical exploration can be helpful.",
    "Spiritual Distress - Conflict with Spiritual Beliefs": "Seek guidance from a spiritual advisor or therapist who understands spiritual issues.",
    "Acculturation Stress - Adapting to a New Culture": "Seek support from cultural organizations and connect with others who share similar experiences.",
    "Ageism - Discrimination Based on Age": "Challenge negative stereotypes and advocate for your rights and well-being.",
    "Ableism - Discrimination Against People with Disabilities": "Advocate for inclusivity and challenge discriminatory attitudes and practices.",
    "Racism - Discrimination Based on Race": "Seek support from community groups and engage in self-care to cope with the impact of racism.",
    "Sexism - Discrimination Based on Sex": "Challenge gender stereotypes and advocate for equality.",
    "Homophobia/Transphobia - Discrimination Based on Sexual Orientation/Gender Identity": "Seek support from LGBTQ+ organizations and allies. Practice self-affirmation.",
    "Body Image Issues - Negative Perception of One's Body": "Challenge negative thoughts about your body and focus on body positivity and self-acceptance.",
    "Sleep Disorders (General) - Disturbed Sleep Patterns": "Practice good sleep hygiene and consult a sleep specialist if problems persist.",
    "Insomnia - Difficulty Falling or Staying Asleep": "Establish a relaxing bedtime routine and avoid caffeine and screens before bed.",
    "Hypersomnia - Excessive Daytime Sleepiness": "Consult a doctor to rule out underlying medical conditions and address sleep habits.",
    "Narcolepsy - Sudden Sleep Attacks": "Work with a neurologist to manage symptoms with medication and lifestyle adjustments.",
    "Sleep Apnea - Breathing Interruptions During Sleep": "Seek medical treatment, such as CPAP therapy, to improve breathing during sleep.",
    "Restless Legs Syndrome - Uncomfortable Leg Sensations": "Practice good sleep hygiene and talk to your doctor about potential treatments.",
    "Nightmares - Distressing Dreams": "Address any underlying trauma or stress. Imagery rehearsal therapy may be helpful.",
    "Sleep Terrors - Episodes of Screaming and Fear During Sleep": "Ensure a safe sleep environment and address any underlying sleep disorders.",
    "Sleepwalking - Walking or Performing Other Behaviors While Asleep": "Ensure a safe sleep environment and address any underlying sleep disorders or triggers.",
    "Bruxism (Teeth Grinding) - Grinding or Clenching Teeth": "Manage stress and consider using a mouthguard at night.",
    "Cognitive Decline - Memory and Thinking Problems": "Seek medical evaluation to determine the cause and explore strategies to manage cognitive changes.",
    "Mild Cognitive Impairment - Subtle Changes in Cognition": "Engage in mentally stimulating activities and maintain a healthy lifestyle.",
    "Dementia (e.g., Alzheimer's Disease) - Progressive Cognitive Decline": "Focus on providing support and a structured environment for the individual and their caregivers.",
    "Delirium - Sudden Confusion and Change in Awareness": "Seek immediate medical attention to identify and treat the underlying medical cause.",
    "Factitious Disorder - Faking Illness for Attention": "Seek mental health treatment to address the underlying psychological needs.",
    "Illness Anxiety Disorder (Hypochondriasis) - Excessive Worry About Health": "Engage in therapy, such as CBT, to address health anxieties and maladaptive beliefs.",
    "Conversion Disorder - Physical Symptoms Without Medical Explanation": "Seek therapy to address the psychological factors contributing to the physical symptoms.",
    "Pain Disorder - Chronic Pain Influenced by Psychological Factors": "Work with a multidisciplinary team to manage pain through physical therapy, medication, and psychological support.",
    "Premenstrual Dysphoric Disorder (PMDD) - Severe PMS Symptoms": "Track your cycle and explore coping strategies like exercise and stress management. Medication may be helpful.",
    "Postpartum Depression - Depression After Childbirth": "Seek immediate support from a doctor or mental health professional. Therapy and medication can be effective.",
    "Menopause-Related Mood Changes": "Explore hormonal therapy options with your doctor and seek emotional support.",
    "Gender Dysphoria - Distress Due to Mismatch Between Gender Identity and Assigned Sex": "Seek support from therapists specializing in gender identity issues and explore transition options if desired.",
    "Paraphilias - Intense Sexual Interests That May Cause Distress or Harm": "Seek therapy to address problematic sexual interests and develop healthy sexual expression.",
    "Sexual Dysfunctions - Difficulties with Sexual Response": "Explore potential physical and psychological causes and seek appropriate medical or psychological treatment.",
    "Domestic Violence - Experiencing Abuse in a Relationship": "Seek immediate safety and support from domestic violence resources and shelters.",
    "Child Abuse - Experiencing Abuse as a Child": "Seek therapy to process the trauma and its long-term effects.",
    "Bullying - Experiencing Harassment or Aggression": "Seek support from trusted adults or organizations that address bullying.",
    "Cyberbullying - Online Harassment": "Document the abuse and seek help from school administrators or online platforms.",
    "Financial Stress - Worrying About Money": "Create a budget and seek financial counseling if needed.",
    "Academic Stress - Pressure Related to School or Studies": "Develop effective study habits and time management skills. Practice stress-reducing techniques.",
    "Career Stress - Pressure and Dissatisfaction at Work": "Identify sources of stress and explore strategies for work-life balance and career satisfaction.",
    "Social Isolation Due to Stigma - Feeling Cut Off Because of Mental Health": "Connect with support groups and advocate for mental health awareness to reduce stigma.",
    "Internalized Stigma - Negative Beliefs About Oneself Due to Mental Illness": "Challenge negative self-talk and focus on your strengths and resilience.",
    "Lack of Access to Mental Health Care": "Advocate for better access and explore available resources in your community or online.",
    "Feeling Misunderstood - Lack of Empathy from Others": "Communicate your experiences clearly and seek support from those who are understanding and empathetic."
}

df = pd.DataFrame(list(data.items()), columns=['category', 'tip'])
df.head()

# ----------------------------
# WHO Mental Health API (Mocked)
# ----------------------------
def get_who_mental_health_resources():
    return [
        {"title": "WHO Mental Health Hub", "url": "https://www.who.int/teams/mental-health-and-substance-use"},
        {"title": "Crisis Helpline (WHO Directory)", "url": "https://www.who.int/mental_health/en/"},
        {"title": "Mental Health Self-Help Toolkit", "url": "https://www.who.int/publications/i/item/9789240035119"}
    ]

# ----------------------------
# Load model & encode categories
# ----------------------------
print("🔄 Loading model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# Get unique categories from the DataFrame
categories = df['category'].unique().tolist()

# Encode categories
category_embeddings = model.encode(df['category'].tolist(), convert_to_tensor=True)

# ----------------------------
# Function: get relevant tip from most similar category
# ----------------------------
import random
from sentence_transformers import util

def get_relevant_tip(user_input):
    # Encode the user input
    user_embedding = model.encode(user_input, convert_to_tensor=True, device=device)

    # Compute similarity with category embeddings
    similarity_scores = util.cos_sim(user_embedding, category_embeddings)
    best_match_idx = similarity_scores.argmax().item()

    # Get the best matched category
    matched_category = categories[best_match_idx]

    # Filter tips from the DataFrame for the matched category
    tips_for_category = df[df["category"] == matched_category]["tip"].tolist()
    selected_tip = random.choice(tips_for_category) if tips_for_category else "No tip available for this category."

    return f"🌿 Based on what you said, here's a helpful suggestion:\n\n📂 Category: {matched_category}\n💡 Tip: {selected_tip}"



# ----------------------------
# Console-based chatbot
# ----------------------------
if __name__ == "__main__":
    print("\n🌱 Welcome to the Self-Care Recommendation System 🌱")
    while True:
        user_input = input("\nHow can I assist you with self-care today? (type 'exit' to quit)\n> ")
        if user_input.lower() in ["exit", "quit"]:
            print("\nTake care! You're not alone. 💚")
            break
        try:
            response = get_relevant_tip(user_input)
            print("\n" + response)

            print("\n📞 Verified Mental Health Resources (WHO):")
            for res in get_who_mental_health_resources():
                print(f"- {res['title']}: {res['url']}")
            print("\n------------------------------")
        except Exception as e:
            print(f"⚠️ Oops, something went wrong: {e}")