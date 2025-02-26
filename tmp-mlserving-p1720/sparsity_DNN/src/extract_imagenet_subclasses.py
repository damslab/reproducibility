from imagenet_classes import IMAGENET2012_CLASSES

def get_subset_labels(keyword:str):

    keywords = {
                'traffic': [
                            "car", "truck", "bus", "bike", "motorcycle", "road", "highway",
                            "vehicle", "train", "tram", "taxi", "ambulance", "fire engine",
                            "airplane", "aircraft", "helicopter", "boat", "ship", "ferry", "traffic",
                            "crosswalk", "street", "bicycle", "scooter", "van", "sedan", "wagon", "jeep"
                        ],
                'animals': [
                            "dog", "cat", "bird", "fish", "insect", "reptile", "amphibian", "mammal",
                            "bear", "tiger", "lion", "zebra", "whale", "snake", "lizard", "frog", 
                            "crab", "octopus", "dolphin", "shark", "penguin", "eagle", "bat", "mouse",
                            "rat", "rabbit", "seal", "spider", "ant", "bee", "horse", "goat", "sheep",
                            "wolf", "fox", "squirrel", "deer", "crocodile", "lobster", "snail",
                            "jellyfish", "seahorse", "dragonfly", "butterfly", "owl", "hawk", "elephant"
                        ],
                'fruits': [
                                "apple",
                                "banana",
                                "cherry",
                                "grape",
                                "orange",
                                "lemon",
                                "lime",
                                "peach",
                                "pear",
                                "pineapple",
                                "plum",
                                "strawberry",
                                "watermelon",
                                "fig",
                                "coconut",
                                "pomegranate",
                                "mango",
                                "kiwi",
                                "papaya",
                                "guava"
                        ],
                'veggies': [
                                "carrot",
                                "potato",
                                "tomato",
                                "onion",
                                "garlic",
                                "cucumber",
                                "broccoli",
                                "cauliflower",
                                "cabbage",
                                "lettuce",
                                "spinach",
                                "pepper",
                                "zucchini",
                                "pumpkin",
                                "eggplant",
                                "radish",
                                "beet",
                                "asparagus",
                                "celery",
                                "turnip",
                                "sweet potato",
                                "squash",
                                "artichoke",
                                "jackfruit"
                        ],
                    'food': [
                                "bread",
                                "cheese",
                                "pizza",
                                "hamburger",
                                "hot dog",
                                "sandwich",
                                "cake",
                                "ice cream",
                                "chocolate",
                                "pasta",
                                "rice",
                                "noodles",
                                "fried egg",
                                "sushi",
                                "taco",
                                "burrito",
                                "dumpling",
                                "steak",
                                "pancake",
                                "waffle",
                                "donut",
                                "croissant",
                                "butter"
                        ],
                    'clothes': [
                                "shirt",
                                "t-shirt",
                                "blouse",
                                "sweater",
                                "jacket",
                                "coat",
                                "dress",
                                "skirt",
                                "jeans",
                                "trousers",
                                "pants",
                                "shorts",
                                "scarf",
                                "hat",
                                "cap",
                                "gloves",
                                "mittens",
                                "socks",
                                "shoes",
                                "sandals",
                                "boots",
                                "tie",
                                "bow tie",
                                "belt",
                                "vest",
                                "hoodie",
                                "overalls",
                                "swimsuit",
                                "bikini",
                                "pajamas",
                                "robe",
                                "raincoat",
                                "blazer",
                                "trunks"
                        ]
                 }
    # Read and filter lines based on keywords
    subset_classes = []

    for k, v in IMAGENET2012_CLASSES.items():
        if any(keyword in v.lower() for keyword in keywords[keyword]):
            subset_classes.append(k)
    
    return subset_classes