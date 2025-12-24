import re
import sys
import pandas as pd
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
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

        self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1,3))
        self.model = RandomForestClassifier(n_estimators=300, random_state=42, max_depth=25)
        
        self.is_trained = False
        self._has_ml_data = False


    # ------------------- Merchant Extractor -------------------
    def _extract_merchant(self, desc: str) -> str:
        desc = str(desc).lower()
        patterns = [
            r"upi[/\-]([^/\-]+)[/\-]",
            r"pos.*?([a-z\s]{3,}?)(?:\s+\d|\s*$)",
            r"transfer[^a-z]*([a-z\s]{3,}?)(?:\s+\d|\s*$)",
        ]
        for pattern in patterns:
            match = re.search(pattern, desc)
            if match:
                merchant = re.sub(r"[^a-z\s]", " ", match.group(1))
                merchant = re.sub(r"\s+", " ", merchant).strip()
                return merchant
        return ""


    # ------------------- Person Detection -------------------
    def _is_person(self, merchant: str, desc: str) -> bool:
        if not merchant:
            return False
        merchant = merchant.lower()
        desc = desc.lower()
        words = merchant.split()

        business_words = ["ltd","pvt","services","solutions","enterprises","store","mart","market","rail","hotel","restaurant","bazaar","agency"]
        if any(bw in merchant for bw in business_words):
            return False

        for word in words:
            if word in self.person_names:
                return True
            for name in self.person_names:
                if len(name)>=4 and name in word:
                    return True

        if ("upi" in desc or "imps" in desc or "neft" in desc):
            if 2 <= len(words) <= 3 and all(w.isalpha() for w in words):
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


    # ------------------- Training -------------------
    def train(self, csv_files: List[str]):
        frames = []
        for file in csv_files:
            print("Reading:", file)
            df = pd.read_csv(file)
            frames.append(df)

        df = pd.concat(frames, ignore_index=True)

        merchants = []
        labels = []
        confs = []
        ml_texts = []

        for d in df["Description"]:
            merchant = self._extract_merchant(d)
            merchants.append(merchant)
            cat, conf = self._rule_classify(d)
            labels.append(cat)
            confs.append(conf)
            clean = re.sub(r"[^a-zA-Z\s]"," ", d.lower())
            ml_texts.append(merchant + " " + clean)

        df["Merchant"] = merchants
        df["Rule_Category"] = labels
        df["Rule_Confidence"] = confs
        df["ML_Text"] = ml_texts

        clean_df = df[df["Rule_Confidence"] >= 0.85]
        clean_df = clean_df[clean_df["Rule_Category"] != "Other"]

        print("Training samples:", len(clean_df))

        if len(clean_df) < 10:
            print("Not enough samples for ML — using rule-based only")
            return df

        X = self.vectorizer.fit_transform(clean_df["ML_Text"])
        y = clean_df["Rule_Category"]

        self.model.fit(X, y)
        self.is_trained = True
        self._has_ml_data = True

        return df


    # ------------------- Prediction -------------------
    def predict(self, desc: str):
        rule_cat, rule_conf = self._rule_classify(desc)

        if rule_conf >= 0.90:
            return rule_cat, rule_conf

        if not self.is_trained:
            return rule_cat, rule_conf

        merchant = self._extract_merchant(desc)
        clean = re.sub(r"[^a-zA-Z\s]"," ", desc.lower())
        text = merchant + " " + clean
        vec = self.vectorizer.transform([text])

        ml_cat = self.model.predict(vec)[0]
        ml_conf = max(self.model.predict_proba(vec)[0])

        if ml_conf * 0.90 > rule_conf:
            return ml_cat, ml_conf * 0.90
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
classifier = OptimizedFinalClassifier()

train_df = classifier.train([
    "9ba9952e_AccountStatement_01-Sep-2025_30-Nov-2025__STD_KOTAK.csv"
])

train_df.head()
classifier.classify_files([
    "9ba9952e_AccountStatement_01-Sep-2025_30-Nov-2025__STD_KOTAK.csv"
])
