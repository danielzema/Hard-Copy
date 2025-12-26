import random

quotes = [
    "Act as if it were impossible to fail - Dorothea Brande",
    "Well begun is half done - Aristotle",
    "Fortune favors the bold - Virgil",
    "Wherever you go, go with all your heart - Confucius",
    "Energy flows where attention goes",
    "What we think, we become - Buddha",
    "Stay hungry, stay foolish - Steve Jobs",
    "The harder the battle, the sweeter the victory - Les Brown",
    "Dream big and dare to fail - Norman Vaughan",
    "You miss 100% of the shots you don't take - Wayne Gretzky",
    "Turn wounds into wisdom - Oprah Winfrey",
    "Small steps lead to big changes",
    "Fall seven times, stand up eight",
    "Do one thing every day that scares you - Eleanor Roosevelt",
    "Action is the foundational key to success - Picasso",
    "Everything is figureoutable - Marie Forleo",
    "Begin anywhere - John Cage",
    "Believe you can and you're halfway there - T. Roosevelt",
    "Courage grows with action",
    "Doubt kills more dreams than failure - Suzy Kassem",
    "Fortune sides with him who dares - Virgil",
    "Great deeds are done by small acts",
    "Keep going. Be all in.",
    "No pressure, no diamonds - Thomas Carlyle",
    "Nothing worth having comes easy - Roosevelt",
    "Opportunities multiply as they are seized - Sun Tzu",
    "Progress, not perfection",
    "Risk more than others think safe - Howard Schultz",
    "Success is never final - Winston Churchill",
    "The best way out is through - Robert Frost",
    "The journey is the reward",
    "The only way is forward",
    "To win, begin - Horace",
    "Turn pain into power",
    "What you do today matters",
    "Work hard in silence - Frank Ocean",
    "You are stronger than you think",
    "Your vibe attracts your tribe",
    "Stay patient and trust your journey",
    "Do good and good will come to you",
    "Go the extra mile",
    "Success demands effort",
    "Dream. Believe. Achieve.",
    "Lead by example",
    "Live less out of habit, more out of intent",
    "Start where you are, use what you have - Arthur Ashe",
    "Simplicity is the ultimate sophistication - Da Vinci",
    "Move fast and break things - Mark Zuckerberg",
    "Be the change you seek - Gandhi",
    "If not now, when?",
    "Grow through what you go through",
    "Make your life a masterpiece - Brian Tracy",
    "Keep moving forward - Walt Disney",
    "Persistence guarantees results - Yogananda",
    "Be fearless in pursuit of your goals",
    "Discipline equals freedom - Jocko Willink",
    "Every moment is a fresh beginning - T.S. Eliot",
    "Hustle beats talent - Ross Simmonds",
    "If you fail, fail forward - John Maxwell",
    "All limitations are self-made",
    "Choose progress over perfection",
    "Don’t wait. Create.",
    "Growth begins at the end of comfort",
    "Hard work beats luck",
    "Impossible is nothing - Muhammad Ali",
    "Joy is a choice",
    "Less talk, more action",
    "Make today count",
    "No rain, no flowers",
    "Outwork yesterday",
    "Prove them wrong",
    "Rise and shine",
    "See the good",
    "Start small, think big",
    "The time is now",
    "Think less, do more",
    "This too shall pass",
    "Today is a new chance",
    "Try again. Repeat.",
    "What you seek is seeking you - Rumi",
    "Winners never quit - Vince Lombardi",
    "You are enough",
    "Your only limit is you",
    "Your future starts today",
    "Better an oops than a what if",
    "Choose courage over comfort - Brené Brown",
    "Decide. Commit. Succeed.",
    "Do more of what matters",
    "Focus on what you can control",
    "Give your best today",
    "Good things take time",
    "Hope is a waking dream - Aristotle",
    "Keep your face to the sun - Helen Keller",
    "Learn by doing - Aristotle",
    "Live boldly",
    "Make your move",
    "Never stop learning",
    "One day or day one. You decide.",
    "Start before you're ready",
    "Success loves speed",
    "The best is yet to come",
    "Trust the process",

    # Mina egna quotes
    "Overperform"
    "Don’t procrastinate"
    "Never face the same problem twice"
    "Morior Invictus"
    "The cold water doesn’t get warmer the longer you wait"
    "Mediocrity doesn’t just happen. It’s chosen over time through small choices day by day"
    "If you spend your time chasing butterflies, they’ll fly away. But if you spend time making a beautiful garden, the butterflies will come to you"
    "You can’t heal in the places you get hurt"
    "A tree falls the way it leans"
    "Wake up early if you want another man’s life or land. No lamb for the lazy wolf. No battle’s won in bed - Havamal"
    "A candle loses no light when lighting another candle"
    "Misogi"
    "A bit of fragrance always clings to the hand that gives roses - A Chinese Proverb"
    "The axe forgets, but the tree remembers - An African Proverb"
    "What you do in private shapes who you are in public"
    "Live in binary: You are either locked in or its playtime, the middleground is where you get destroyed"
]

# Choose one at random
def get_random_quote():
    return random.choice(quotes)
