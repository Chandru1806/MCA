import re
import sys
import pandas as pd
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
class OptimizedFinalClassifier:
    def __init__(self) -> None:
        # =============================
        # 1. MASTER CATEGORY KEYWORDS
        # =============================
        self.categories = {
            "Food": [
                "zomato", "swiggy", "dominos", "thearogya", "grandmaslil",
                "asanbaibiriyani", "kitchenking", "frozen bottle",
                "chulhachaukida", "manjal", "madrascoffee", "edenparkcafete",
                "sukkubhaifoodspriv", "avs enterprises", "blossombook",
                "mdp food", "mdpfood", "mdp food a",
                "hotel sree vijayalaksh", "hotel sree vijayalakshtoran",
                "hotel sree", "narasus", "narasus coffee",
                "murugan idli", "muru gan idli",
            ],
            "Shopping": [
                "amazon", "flipkart", "myntra", "westside", "reliancedigital",
                "decathlon", "zudio", "max retail", "snitchapparels",
                "greentrends", "nagarjunaandhra", "sublrelements",
                "mssterlingdeco", "purple gra", "gocolors", "go colors",
                "the chennai silks","chennai silks","world of titan",
                "worl d of tit","new cotton collection","cotton collection",
                "maha sports","sports design","tamil nadu thunikkadai","thunikkadai",
            ],
            "Travel": [
                "redbus","irctc","uber","ola","indianrailways","indian railways",
                "indian rai","chennaimetrorail","metropolitan transpo",
                "indigo","iatapay","iata pay","indigo.iatapay",
            ],
            "Bills": [
                "airtel","jio","bsnl","tataplay","tangedco","airtelpayments",
                "airteldirectupipo","jiohotstar","tataplayfiber",
                "rbmlsolutionsindia","icicimerchantservi","avighnaenterprises",
                "eb bill","electricity bill",
            ],
            "Entertainment": ["netflix","bookmyshow","bigtree","my11circle","wwwwoohoo","executive lounge"],
            "Subscriptions": ["appleservices","openai","chatgp","youtube","youtubecybss"],
            "Health": ["apollo","shreeramdev medical","santhanam pharmacy","mercury","apollo pharm","apollo pharmacy"],
            "Groceries": [
                "zepto","zeptonow","zeptomarketplace","amazonpay groceries",
                "easybazar","cn2easybazarsupe","cn1easybazarsuper","kpnfarmfresh",
                "shopwel mart","spar2167elemen","grace supermark","loyal worl",
                "loyal world","aswins hom","aswins home","sri maha superm",
                "sri maha super market","sri maha super", "super market",
            ],
            "Education": ["anna university","ccaannauniversity","apdfgurucom"],
            "Fuel": ["parsons fuels","shreelpkpetropa","banu fuels","petrol bunk","fuel station"],
        }

        self.person_names = {
            "murugadoss","rizwan","mugesh","srinivasan","sriramappab","aadyabanashankari",
            "afroz","manikandan","vabhinesh","chandragiriya","kunde","varun","mudassir",
            "shariff","govindagouda","ramanag","surinenianjali","dhanikachalam",
            "rahmathulla","khan","sivaprakash","raja","meenakshi","radhakrish",
            "balamurali","elangovan","palakolanu","venkata","ashanmuga","sundaram",
            "mrsuresh","punith","moneiruddin","laskar","harshavardhan","niranjansubba",
            "hegde","prdeep","kumar","prakash","kalimuthu","thajudeen","mrahamed",
            "ali","gnanasekar","akash","saiganesh","santhanam","bharathkumar","maari",
            "anil","sindhukumar","rmahesh","kumaresan","kuppan","theirani","madaraje",
            "urs","manjula","olekar","ancy","anand","venu","rahul","sriram","rukmani",
            "goutham","gouthamram","kamalesh","bagyaraj","selvamani","himakiran",
            "sandeep","prasath","paramasivan",
        }

        self.regex_rules = [
            (re.compile(r"fastag|fasttag|toll", re.IGNORECASE), "Travel", 0.90),
            (re.compile(r"\bhotel\b", re.IGNORECASE), "Food", 0.80),
            (re.compile(r"(super\s*market|supermart|mart\b)", re.IGNORECASE),"Groceries",0.80),
            (re.compile(r"chennai\s*silks", re.IGNORECASE),"Shopping",0.90),
            (re.compile(r"world\s+of\s+titan", re.IGNORECASE),"Shopping",0.90),
            (re.compile(r"cotton\s+collection", re.IGNORECASE),"Shopping",0.90),
            (re.compile(r"by\s+transfer.*(neft|imps|inb)", re.IGNORECASE),"Internal_Transfer",0.85),
        ]

        print("Loading semantic model...")
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.category_embeddings = None
        self._init_category_embeddings()
        print("Model loaded successfully")


    # ------------------- Initialize Category Embeddings -------------------
    def _init_category_embeddings(self):
        category_examples = {
            "Food": ["restaurant payment", "food delivery zomato swiggy", "hotel dining cafe", "biryani pizza burger"],
            "Shopping": ["online shopping amazon flipkart", "clothing store myntra", "retail purchase decathlon", "fashion apparel"],
            "Travel": ["train ticket irctc", "flight booking indigo", "uber ola cab ride", "metro bus transport", "fastag toll"],
            "Bills": ["electricity bill payment", "mobile recharge airtel jio", "internet broadband", "utility payment"],
            "Entertainment": ["netflix subscription", "movie ticket bookmyshow", "gaming entertainment"],
            "Subscriptions": ["monthly subscription", "youtube premium", "apple services", "recurring payment"],
            "Health": ["pharmacy medicine", "hospital apollo", "medical store", "healthcare"],
            "Groceries": ["supermarket shopping", "grocery store", "vegetables fruits", "zepto blinkit"],
            "Education": ["university fees", "course payment", "educational institution"],
            "Fuel": ["petrol pump", "diesel fuel station", "gas refill"],
            "Person": ["transfer to person", "upi payment to individual", "money sent to friend", "personal transfer"],
            "ATM": ["atm withdrawal", "cash withdrawal", "atm transaction"],
            "Salary": ["salary credit", "monthly salary", "income payment"],
            "Interest": ["interest credited", "bank interest", "savings interest"],
            "Refund": ["refund received", "amount refunded", "reversal transaction"],
            "Internal_Transfer": ["account transfer", "self transfer", "internal fund transfer"],
        }
        
        all_examples = []
        self.category_map = []
        for cat, examples in category_examples.items():
            for ex in examples:
                all_examples.append(ex)
                self.category_map.append(cat)
        
        self.category_embeddings = self.semantic_model.encode(all_examples)

    # ------------------- Merchant Extractor -------------------
    def _extract_merchant(self, desc: str) -> str:
        desc_lower = str(desc).lower()
        
        # UPI: Extract 4th field (merchant/person name)
        upi_match = re.search(r"upi[/\-][^/\-]+[/\-][^/\-]+[/\-]([^/\-]+)", desc_lower)
        if upi_match:
            merchant = re.sub(r"[^a-z\s]", " ", upi_match.group(1))
            return re.sub(r"\s+", " ", merchant).strip()
        
        # POS: Extract merchant before location
        pos_match = re.search(r"pos\d+([a-z\s]{3,}?)(?:che|ban|mum|del|hyd|pun|kol)", desc_lower)
        if pos_match:
            merchant = re.sub(r"[^a-z\s]", " ", pos_match.group(1))
            return re.sub(r"\s+", " ", merchant).strip()
        
        # IMPS/NEFT: Extract name field
        transfer_match = re.search(r"(?:imps|neft)[/\-][^/\-]+[/\-]([^/\-]+)", desc_lower)
        if transfer_match:
            merchant = re.sub(r"[^a-z\s]", " ", transfer_match.group(1))
            return re.sub(r"\s+", " ", merchant).strip()
        
        return ""


    # ------------------- Person Detection -------------------
    def _is_person(self, merchant: str, desc: str) -> bool:
        if not merchant or len(merchant) < 3:
            return False
        
        merchant_lower = merchant.lower()
        desc_lower = desc.lower()
        
        business_words = ["ltd","pvt","services","solutions","enterprises","store","mart","market","rail","hotel","restaurant","bazaar","agency","paytm","google","zomato","swiggy","irctc","airtel","bmtc","amazon","flipkart"]
        if any(bw in merchant_lower for bw in business_words):
            return False

        merchant_words = merchant_lower.split()
        for word in merchant_words:
            if len(word) >= 4:
                for name in self.person_names:
                    if name in word or word in name:
                        return True

        if ("upi" in desc_lower or "imps" in desc_lower or "neft" in desc_lower):
            if 2 <= len(merchant_words) <= 4 and all(len(w) >= 3 and w.isalpha() for w in merchant_words):
                return True

        return False


    # ------------------- Rule Classifier -------------------
    def _rule_classify(self, description: str) -> Tuple[str, float]:
        desc = description.lower()
        merchant = self._extract_merchant(description)

        if any(w in desc for w in ["nwd","atm wdl","atm cash"]):
            return "ATM", 0.95

        if ("interestpaid" in desc or "credit interest" in desc):
            return "Interest", 0.95

        if "bulk posting" in desc and "ppo" in desc:
            return "Salary", 0.90

        if "csh dep (cdm)" in desc:
            return "Internal_Transfer", 0.85

        if "salary" in desc:
            return "Salary", 0.95

        if "refund" in desc or "rev-upi" in desc:
            return "Refund", 0.90

        for pattern, cat, conf in self.regex_rules:
            if pattern.search(desc):
                return cat, conf

        for cat, patterns in self.categories.items():
            for p in patterns:
                if p in merchant or p in desc:
                    return cat, 0.90

        if self._is_person(merchant, desc):
            return "Person", 0.85

        return "Other", 0.30


    # ------------------- Semantic Classification -------------------
    def _semantic_classify(self, description: str) -> Tuple[str, float]:
        desc_embedding = self.semantic_model.encode([description])
        similarities = cosine_similarity(desc_embedding, self.category_embeddings)[0]
        
        best_idx = np.argmax(similarities)
        best_category = self.category_map[best_idx]
        confidence = float(similarities[best_idx])
        
        # Aggregate scores by category
        category_scores = {}
        for idx, cat in enumerate(self.category_map):
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(similarities[idx])
        
        # Use max similarity for each category
        final_scores = {cat: max(scores) for cat, scores in category_scores.items()}
        best_cat = max(final_scores, key=final_scores.get)
        best_conf = final_scores[best_cat]
        
        return best_cat, best_conf

    # ------------------- Training (Simplified) -------------------
    def train(self, csv_files: List[str]):
        frames = []
        for file in csv_files:
            print("Reading:", file)
            df = pd.read_csv(file)
            frames.append(df)

        df = pd.concat(frames, ignore_index=True)
        print(f"Total transactions: {len(df)}")
        return df


    # ------------------- Prediction -------------------
    def predict(self, desc: str):
        # Step 1: Rule-based classification (high confidence cases)
        rule_cat, rule_conf = self._rule_classify(desc)
        
        if rule_conf >= 0.90:
            return rule_cat, rule_conf
        
        # Step 2: Semantic classification for low confidence cases
        semantic_cat, semantic_conf = self._semantic_classify(desc)
        
        # Step 3: Choose best prediction
        if semantic_conf > rule_conf:
            # Adjust confidence based on semantic score ranges
            if semantic_conf >= 0.50:
                adjusted_conf = 0.70 + (semantic_conf - 0.50) * 0.5  # Maps 0.50-1.0 to 0.70-0.95
            else:
                adjusted_conf = semantic_conf * 1.4  # Boost lower scores
            
            return semantic_cat, min(adjusted_conf, 0.95)
        
        return rule_cat, rule_conf


    # ------------------- Classify Full CSV -------------------
    def classify_files(self, csv_files: List[str]):
        for file in csv_files:
            print("Classifying:", file)
            df = pd.read_csv(file)

            out_cat = []
            out_conf = []

            for d in df["Description"]:
                cat, conf = self.predict(d)
                out_cat.append(cat)
                out_conf.append(conf)

            df["Category"] = out_cat
            df["Confidence"] = out_conf

            outfile = file.replace(".csv", "_optimized_final.csv")
            df.to_csv(outfile, index=False)
            print("Written:", outfile)
if __name__ == "__main__":
    import os
    
    # Get outputs directory
    outputs_dir = os.path.join("..", "..", "storage", "outputs")
    
    # List all CSV files
    csv_files = [f for f in os.listdir(outputs_dir) if f.endswith('.csv') and not f.endswith('_optimized_final.csv')]
    
    if not csv_files:
        print("No CSV files found in storage/outputs/")
    else:
        print("\n=== Available CSV Files ===")
        for idx, file in enumerate(csv_files, 1):
            print(f"{idx}. {file}")
        
        choice = input("\nEnter file number to categorize (or 'all' for all files): ").strip()
        
        classifier = OptimizedFinalClassifier()
        
        if choice.lower() == 'all':
            selected_files = [os.path.join(outputs_dir, f) for f in csv_files]
        else:
            try:
                idx = int(choice) - 1
                selected_files = [os.path.join(outputs_dir, csv_files[idx])]
            except (ValueError, IndexError):
                print("Invalid choice!")
                exit(1)
        
        classifier.classify_files(selected_files)
        print("\n✓ Categorization complete!")
